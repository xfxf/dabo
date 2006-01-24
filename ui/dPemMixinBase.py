""" dPemMixin.py: Provide common PEM functionality """
import dabo
import types
from dabo.dObject import dObject
from dabo.dLocalize import _


class dPemMixinBase(dObject):
	""" Provide Property/Event/Method interfaces for dForms and dControls.

	Subclasses can extend the property sheet by defining their own get/set
	functions along with their own property() statements.
	"""
	def _initEvents(self):
		super(dPemMixinBase, self)._initEvents()
		self.autoBindEvents()

	def _initUI(self):
		""" Abstract method: subclasses MUST override for UI-specifics.
		"""
		pass
	
	def getPropertyInfo(cls, name):
		""" Abstract method: subclasses MUST override for UI-specifics.
		"""
		return super(dPemMixinBase, cls).getPropertyInfo(name)
	getPropertyInfo = classmethod(getPropertyInfo)
	
	def addObject(self, classRef, name=None, *args, **kwargs):
		""" Create an instance of classRef, and make it a child of self.
		
		Abstract method: subclasses MUST override for UI-specifics.
		"""
		pass
		

	def reCreate(self, child=None):
		""" Abstract method: subclasses MUST override for UI-specifics.
		"""
	
	def clone(self, obj, name=None):
		""" Abstract method: subclasses MUST override for UI-specifics.
		"""
		pass


	def _initName(self, name=None, _explicitName=True):
		if name is None:
			name = self.Name
		try:
			self._setName(name, _userExplicit=_explicitName)
		except AttributeError:
			# Some toolkits (Tkinter) don't let objects change their
			# names after instantiation.
			pass

			
	def _processName(self, kwargs, defaultName):
		# Called by the constructors of the dObjects, to properly set the
		# name of the object based on whether the user set it explicitly
		# or Dabo is to provide it implicitly.
		_explicitName = kwargs.get("_explicitName", False)
		
		if "Name" in kwargs.keys():
			if "_explicitName" not in kwargs.keys():
				# Name was sent; _explicitName wasn't.
				_explicitName = True
			name = kwargs["Name"]
		else:
			name = defaultName

		if kwargs.has_key("_explicitName"):
			del(kwargs["_explicitName"])
		return name, _explicitName
		


	# Scroll to the bottom to see the property definitions.

	# Property get/set/delete methods follow.
	
		
	def _getForm(self):
		""" Return a reference to the containing Form. 
		"""
		try:
			return self._cachedForm
		except AttributeError:
			import dabo.ui
			obj, frm = self, None
			while obj:
				try:
					parent = obj.Parent
				except AttributeError:
					break
				if isinstance(parent, (dabo.ui.dFormMixin)):
					frm = parent
					break
				else:
					obj = parent
			if frm:
				self._cachedForm = frm   # Cache for next time
			return frm


	def _getBottom(self):
		return self.Top + self.Height
	def _setBottom(self, bottom):
		self.Top = int(bottom) - self.Height

	def _getRight(self):
		return self.Left + self.Width
	def _setRight(self, right):
		self.Left = int(right) - self.Width




	# Property definitions follow
	Bottom = property(_getBottom, _setBottom, None,
					'The position of the bottom part of the object. (int)')
	
	Form = property(_getForm, None, None,
					'Object reference to the dForm containing the object. (read only).')
	
	Right = property(_getRight, _setRight, None,
					'The position of the right part of the object. (int)')


if __name__ == "__main__":
	o = dPemMixin()
	print o.BaseClass
	o.BaseClass = "dForm"
	print o.BaseClass
