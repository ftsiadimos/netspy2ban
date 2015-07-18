import wx
import wx.lib.agw.toasterbox as TB
a= 1
def toster(self, mess):
        toaster = TB.ToasterBox(self, tbstyle=TB.TB_SIMPLE)
        toaster.SetTitle('NetSpy2Ban')
        toaster.SetPopupPauseTime(4000)
        toaster.SetPopupBackgroundColour("BLACK")
        toaster.SetPopupPositionByInt(0)
        toaster.SetPopupScrollSpeed(10)
        toaster.SetPopupSize((400,100))
        toaster.SetPopupTextColour("RED")
        toaster.SetPopupText(mess)
	if a == 1:
        	wx.CallLater(1000, toaster.Play)
