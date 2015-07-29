#!/usr/bin/python
""" Popup messages """
# -*- coding: utf-8 -*-
# Copyright 2015 Fotios Tsiadimos
# Licensed under the terms of the GPL License
# (see License file for details)


import wx
import wx.lib.agw.toasterbox as TB
POPMSG = 1

def toster(self, event):
    """ Main Mesg Function """
    toaster = TB.ToasterBox(self, tbstyle=TB.TB_SIMPLE)
    toaster.SetTitle('NetSpy2Ban')
    toaster.SetPopupPauseTime(4000)
    toaster.SetPopupBackgroundColour("BLACK")
    toaster.SetPopupPositionByInt(0)
    toaster.SetPopupScrollSpeed(10)
    toaster.SetPopupSize((400, 100))
    toaster.SetPopupTextColour("RED")
    toaster.SetPopupText(event)
    if POPMSG == 1:
        wx.CallLater(1000, toaster.Play)


if __name__ == "__main__":
    print "This is a module for netspy2ban.py"

