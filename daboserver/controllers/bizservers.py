import logging
import pickle
import os
import time
import tempfile
from zipfile import ZipFile

# Create a log
log = logging.getLogger(__name__)

#-------------------------------------------------------
# Pylons-specific imports. If you use a different webserver,
# change this to what your server needs.
from pylons import request, response, session
from pylons import tmpl_context as c
from pylons.controllers.util import abort, redirect_to
#-------------------------------------------------------

#-------------------------------------------------------
# Dabo-specific imports
import dabo
from dabo.dLocalize import _
from daboserver.lib.base import BaseController, render
from dabo.dException import WebServerException
from dabo.lib.manifest import Manifest
#-------------------------------------------------------

#-------------------------------------------------------
# Import the bizobj classes here that will be used in this application
# Then be sure to link them to their DataSource in the 'bizDict' 
# definition below.
## NOTE: the next line is an example from the demonstration app.
## Be sure to CHANGE it to whatever is required for your app.
from OrdersBizobj import OrdersBizobj
#-------------------------------------------------------


# The bizobj class *MUST* be defined here for each data source that is to be 
# handled by this server. Be sure that these classes are imported above.
## NOTE: as mentioned above, this is for the demo app.
bizDict = {"orders": OrdersBizobj}

# The path to the server copy of the web application source files *MUST* be
# defined here. It is used to compare local app manifests in order to 
# determine what changes, if any, have been made to the app. 
sourcePath = os.path.join(os.getcwd(), "daboserver/appSource")



class BizserversController(BaseController):
	
	def biz(self, hashval=None, ds=None, method=None, *args, **kwargs):
		"""This is the main method for handling requests from client bizobjs. It expects 
		the following parameters, which will be obtained from the URL of the request:
			hashval: The value of hash(localBizobj). Used to link local and remote bizobjs.
			ds: The DataSource of the bizobj
			method: The method of the bizobj to be called.
		"""
		params = dict(request.GET)
		bizClass = bizDict.get(ds)
		if not bizClass:
			abort(404, _("DataSource '%s' not found") % ds)
		biz = bizClass.load(hashval, ds)
		try:
			# Get the webserver method that wraps the bizobj call. This is done so that 
			# webserver-specific methods, such as 'abort()' in Pylons, are kept separate
			# from the bizobj.
			serverMethod = getattr(self, method)
			ret = serverMethod(biz, hashval, ds, *args, **kwargs)
		except AttributeError:
			abort(404, _("No such method '%s' found,") % method)
		biz.storeToCache(hashval)
		return ret


	def requery(self, biz, hashval, ds, *args, **kwargs):
		params = request.params
		sql = params.get("SQL")
		kf = params.get("KeyField")
		biz.KeyField = kf
		biz.storeRemoteSQL(sql)
		biz.requery()
		data = biz.getDataSet(returnInternals=True)
		dumped = pickle.dumps(data)
		typs = pickle.dumps(biz.getDataTypes())
		ret = dabo.lib.jsonEncode((dumped, typs))
		return ret


	def save(self, biz, hashval, ds, *args, **kwargs):
		params = request.params
		encdiff = params.get("DataDiff")
		diff = dabo.lib.jsonDecode(encdiff)
		try:
			err = biz.applyDiffAndSave(diff, primary=True)
		except WebServerException, e:
			abort(500, e)
		# 'err' will be None unless an exception was encountered.
		if err:
			# The format is a 2-tuple: (error code, text)
			abort(err[0], err[1])
		data = biz.getDataSet(returnInternals=True)
		typs = pickle.dumps(biz.getDataTypes())
		ret = dabo.lib.jsonEncode((data, typs))
		return ret


	def delete(self, biz, hashval, ds, *args, **kwargs):
		params = request.params
		pk = params.get("PK")
		try:
			biz.moveToPK(pk)
			biz.delete()
		except WebServerException, e:
			abort(500, e)
		data = biz.getDataSet(returnInternals=True)
		typs = pickle.dumps(biz.getDataTypes())
		ret = dabo.lib.jsonEncode((data, typs))
		return ret


	def getFileRequestDB(self):
		curr = os.getcwd()
		db = os.path.join(curr, "DaboFileCache.db")
		cxn = dabo.db.dConnection(connectInfo={"DbType": "SQLite", "Database": db})
		cursor = cxn.getDaboCursor()
		return cursor


	def manifest(self, app, fnc=None, id=None, *args, **kwargs):
		crs = self.getFileRequestDB()
		appPath = os.path.join(sourcePath, app)
		mf = Manifest.getManifest(appPath)
		# Handle the various functions
		if fnc is None or fnc ==  "full":
			# Send the full manifest
			pmf = pickle.dumps(mf)
			ret = dabo.lib.jsonEncode(pmf)
			return ret

		elif fnc == "diff":
			enclocal = request.params.get("current")
			local = dabo.lib.jsonDecode(enclocal)
			chgs = Manifest.diff(mf, local)
			if not chgs:
				abort(304, _("No changes"))
			# The diff will contain both added/updated file, as well as deleted
			# files. Separate the two in case the only change involves deletions.
			nonDelChanges = [kk for (kk, vv) in chgs.items()
					if vv]
			if nonDelChanges:
				# Create a unique val to store the diffs so that the client
				# can request the files.
				hashval = hash((request, time.time()))
				sql = """create table if not exists filecache (
					hashval text, 
					updated int,
					pickledata text)
					"""
				crs.execute(sql)
				updated = int(time.time())
				sql = """insert into filecache (hashval, updated, pickledata)
						values (?, ?, ?)"""
				crs.execute(sql, (hashval, updated, pickle.dumps(chgs)))
			else:
				# No added/updated files. Return a zero filecode to signify nothing to download
				hashval = 0
			# Return the hashval and manifest so that the user can request the files
			retPickle = pickle.dumps((hashval, chgs, mf))
			return dabo.lib.jsonEncode(retPickle)

		elif fnc == "files":
			# The client is requesting the changed files. The hashval will
			# be in the kwargs
			sql = """select pickledata from filecache
					where hashval = ?"""
			crs.execute(sql, (id, ))
			chgs = pickle.loads(crs.Record.pickledata)
			# Need to cd to the source directory
			currdir = os.getcwd()
			os.chdir(appPath)
			fd, tmpname = tempfile.mkstemp(suffix=".zip")
			os.close(fd)
			z = ZipFile(tmpname, "w")
			for pth,tm in chgs.items():
				# File names must be str for zipfile
				pth = str(pth)
				if tm:
					z.write(pth)
			z.close()
			response.headers['content-type'] = "application/x-zip-compressed"
			os.chdir(currdir)
			ret = file(tmpname).read()
			os.remove(tmpname)
			return ret
