""" dFormMain.py """
import wx
import dFormMixin as fm
import dPanel, dIcons
import dabo

import time

# Different platforms expect different frame types. Notably,
# most users on Windows expect and prefer the MDI parent/child
# type frames.

## pkm 06/09/2004: disabled MDI even on Windows. There are some issues that I
## don't have time to track down right now... better if it works
## on Windows similarly to Linux instead of not at all... if you
## want to enable MDI on Windows, just take out the "False and"
## in the below if statement, and do the same in dForm.py.

if False and wx.Platform == '__WXMSW__':	  # Microsoft Windows
	wxFrameClass = wx.MDIParentFrame
	wxPreFrameClass = wx.PreMDIParentFrame
else:
	wxFrameClass = wx.Frame
	wxPreFrameClass = wx.PreFrame


class bgImgPanel(dPanel.dPanel):
	def __init__(self, parent):
		bgImgPanel.doDefault(parent)
		self.bitmap = dIcons.getIconBitmap("dabo_lettering_250x100")
		self.needRedraw = False
		self.szTimer = wx.StopWatch()
		self.bindEvent(dabo.dEvents.Paint, self.onPaint)
		self.bindEvent(dabo.dEvents.Idle, self.onIdle)
		self.bindEvent(dabo.dEvents.Resize, self.onResize)

		## To get the Dabo Icon looking right, this was the easiest, but
		## we'll want to research using a mask in the future.
		self.BackColor = "White"

	def onPaint(self, evt):
		dc = wx.PaintDC(self)
		self.draw(dc)

	def onResize(self, evt):
		self.needRedraw = True
		self.szTimer.Start()
	
	def onIdle(self, evt):
		if self.needRedraw:
			if self.szTimer.Time() < 100:
				return
			dc = wx.ClientDC(self)
			self.draw(dc)
			self.needRedraw = False
			self.szTimer.Pause()

	def draw(self, dc):
		sw = wx.StopWatch()
		sw.Start()
		# This throws a non-fatal error, but I don't know why - 
		# the docs claim that this is perfectly legitimate.
		wd,ht = dc.GetSize()
		# bitmap is 128x128, so compute the scale.
		#dc.SetUserScale( (wd/ 128.0), (ht / 128.0) )
		## pkm: the scaling is ugly and is what was causing the slow
		## response: instead, let's center the bitmap.
		dc.Clear()
		dc.DrawBitmap(self.bitmap, 10, (ht - 110))
		sw.Pause()


class dFormMain(wxFrameClass, fm.dFormMixin):
	""" This is the main top-level form for the application.
	"""
	def __init__(self):

		self._baseClass = dFormMain

		pre = wxPreFrameClass()
		self._beforeInit(pre)				   # defined in dPemMixin
		pre.Create(None, -1, "dFormMain")

		self.PostCreate(pre)
		
		self.Name = "dFormMain"
		self.Size = (640,480)
		self.Position = (0,0)

		fm.dFormMixin.__init__(self)
		
		# Experimental! Places a background image on the main 
		# form. It's slow and the image looks terrible, but it's a start...
		if True:
			self.bg = bgImgPanel(self)
			self.bg.SetPosition( (0,0) )
			self.bg.SetSize( self.GetSize() )

		if wx.Platform != '__WXMAC__':
			self.CreateStatusBar()

		self._afterInit()					   # defined in dPemMixin

		
	def afterInit(self):
		self.Caption = "Dabo"
		self.setStatusText("Welcome to Dabo!")


if __name__ == "__main__":
	import test
	test.Test().runTest(dFormMain)
