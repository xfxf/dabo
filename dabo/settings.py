# -*- coding: utf-8 -*-

import os
import sys

# Dabo Global Settings

# Do not modify this file directly. Instead, create a file called 
# settings_override.py, and copy/paste the settings section below into the 
# settings_override.py file. This way, when you update Dabo, you won't blow 
# away your custom tweaks.

# Note that creating a settings_override.py isn't the only way to tweak the 
# settings - your custom code can also just make the settings in the dabo 
# namespace at runtime, eg:
#
#  import dabo
#  dabo.eventLogging = True
#  <do stuff>
#  dabo.eventLogging = False

# Also note that settings_override.py is not the appropriate place to put 
# application-specific settings, although it may seem at first like an easy 
# place to do so.


### Settings - begin

# Do we write info-level messages to stdout?
verboseLogging = False

# Event logging is turned off globally by default for performance reasons.
# Set to True (and also set LogEvents on the object(s)) to get logging.
eventLogging = False

# Set the following to True to get all the data in the UI event put into
# the dEvent EventData dictionary. Only do that for testing, though,
# because it is very expensive from a performance standpoint.
allNativeEventInfo = False

# Set dabo.fastNameSet to True to bypass Dabo's checking to make sure siblings
# have unique names, greatly speeding up instantiation of many objects. If you
# do this, your code takes responsibility for ensuring that sibling names are
# in fact unique. We recommend you leave fastNameSet to False here, and wrap 
# your object creations around setting it to True. eg:
#
#   dabo.fastNameSet = True
#   for i in range(200):
#     self.addObject(dabo.ui.dButton, Name="b_%s" % i)
#   dabo.fastNameSet = False
fastNameSet = False


# dabo.autoBindEvents is a global flag which determines if events are bound
# automatically to callback functions when the object is instantiated. E.g.,
# where you used to have to have code like:
#
#   def initEvents(self):
#       self.bindEvent(dEvents.MouseEnter, self.onMouseEnter)
#
# with autoBindEvents, all you need to do is define the onMouseEnter function,
# and Dabo will understand that that function should be called upon the
# MouseEnter event. Additionally, if an object has it's RegID set, the form
# can have callbacks of the form on<EventName>_<ObjectName>(), which become
# the callback function for that event and object. E.g.:
#
#   def onMouseEnter_cmdOkay(self, evt):
#       """This gets called when the mouse enters the okay command button."""
#
autoBindEvents = True


# If you set MDI to True, then dFormMain and dForm will default to being MDI
# parent and MDI child, respectively. IOW, you don't have to change your dForm
# and dFormMain subclasses to inherit from dFormChildMDI, etc., but it comes at
# the cost of being a global setting. This must be set before dabo.ui is 
# imported (ie right at the top of your app). Note that you could instead choose
# to deal with MDI/SDI explicitly in your form subclasses. IOW:
#		class MyForm(dabo.ui.dFormChildMDI)
#		class MyForm(dabo.ui.dFormParentMDI)
#		class MyForm(dabo.ui.dFormSDI)
#
# All the MDI setting does is make dFormMain == (dFormMainSDI or dFormMainParentMDI)
# and dForm == (dFormSDI or dFormChildMDI)
MDI = False
# (note: MDI doesn't work at all on Mac as of this writing, and is implemented
#        as a pageframe on Linux. I'm almost thinking we should default to True
#        on Windows though, because it seems to be the arrangement most users
#        expect.)

# macFontScaling: If you set a font to 10 pt it'll look medium-small on most
# Windows and Linux screens. However, it will look very small on Mac because
# of automatic conversion in OS X. 8pt fonts on Mac are barely even readable.
# Set macFontScaling to True to make your fonts appear the same size on all 
# platforms.
macFontScaling = True
 
# When doing date calculations, displaying calendars, etc., this determines whether
# 'Sunday' or 'Monday' is considered the beginning of the week
firstDayOfWeek = "Sunday"

# Default font size when none other is specified
defaultFontSize = 10

# Default language to use when none is specified
defaultLanguage = "en"

# Default encoding to use when none is specified
defaultEncoding = "utf-8"

# Default log file for the dabo.dBug.loggit function
loggitFile = "functionCall.log"

# Does the UI layer (dForm) eat exceptions from the biz layer
# such as 'invalid row specified' or bizrule violations and
# automatically display an informational message to the user (True), 
# or does the exception go unhandled so that the developer can 
# quickly diagnose the issue (False)?
eatBizExceptions = True
 
# Check for web updates?
checkForWebUpdates = True

# Date and Time formats. None will use the os user's settings, but
# your code can easily override these. Example:
#   dabo.settings.dateFormat = "%d.%m.%Y" -> "31.12.2008".
dateFormat = None
dateTimeFormat = None
timeFormat = None

# Do we load the os user's locale settings automatically? 
# Pythonista note: this executes: 
#    locale.setlocale(locale.LC_ALL, '')
loadUserLocale = True

# File extensions understood by the getFile functions. The format is a dictionary, with
# the extension as the key, and the descriptive text as the value. To add your own 
# custom extensions, create a dict with this same format named 'custom_extensions'
# in your settings_override file, and those will be added to this list.
custom_extensions = {}
file_extensions = {
		"*": "All Files",
		"py": "Python Scripts",
		"txt": "Text Files",
		"log": "Log Files",
		"fsxml": "Dabo FieldSpec Files",
		"cnxml": "Dabo Connection Files",
		"rfxml": "Dabo Report Format Files",
		"cdxml": "Dabo Class Designer Files",
		"mnxml": "Dabo Menu Designer Files",
		"pdf": "PDF Files",
		"js": "Javascript Files",
		"html" : "HTML Files",
		"xml" : "XML Files",
		"jpg" : "JPEG Images",
		"jpeg" : "JPEG Images",
		"gif" : "GIF Images",
		"tif" : "TIFF Images",
		"tiff" : "TIFF Images",
		"png" : "PNG Images",
		"ico" : "Icon Images",
		"bmp" : "Bitmap Images",
		"sh": "Shell Scripts",
		"zip": "ZIP Files",
		"tar": "tar Archives",
		"gz": "gzipped Files",
		"tgz": "gzipped tar Archives",
		"mov": "QuickTime Movies",
		"wmv": "Windows Media Videos",
		"mpg": "MPEG Videos",
		"mpeg": "MPEG Videos",
		"mp3": "mp3 Audio Files",
}

# For file-based data backends such as SQLite, do we allow creating a connection to
# a non-existent file, which SQLite will then create? 
createDbFiles = False

# URL of the Web Update server
webupdate_urlbase = "http://daboserver.com/webupdate"


### Settings - end

# Make sure that the current directory is in the sys.path
sys.path.append(os.getcwd())

# Do not copy/paste anything below this line into settings_override.py.
try:
	from settings_override import *
except ImportError:
	pass
