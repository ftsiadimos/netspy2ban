#!/usr/bin/env python
"""  Taskbar """
# -*- coding: utf-8 -*-
#
# Copyright 2015 Fotios Tsiadimos
# Licensed under the terms of the GPL License
# (see License file for details)

import wx

class MyTaskBarIcon(wx.TaskBarIcon):
    """ Main Taskbar Class """
    def __init__(self, frame):
        wx.TaskBarIcon.__init__(self)

        self.frame = frame
        self.SetIcon(wx.Icon("/usr/lib/python2.7/site-packages/netspy2ban/icons/netspy2ban.ico", wx.BITMAP_TYPE_ICO), 'NetSpy2Ban')
        self.Bind(wx.EVT_MENU, self.OnTaskBarActivate, id=1)
        self.Bind(wx.EVT_MENU, self.OnTaskBarDeactivate, id=2)
        self.Bind(wx.EVT_MENU, self.OnTaskBarClose, id=3)
        self.Bind(wx.EVT_TASKBAR_LEFT_DOWN, self.on_left_down)

    def on_left_down(self, event):
        """ Hide the window on left click """
        if self.frame.IsShown():
            self.frame.Hide()
        else:
            self.frame.Show()

    def CreatePopupMenu(self):
        """ Right Menu click """
        menu = wx.Menu()
        menu.Append(1, 'Show')
        menu.Append(2, 'Hide')
        menu.Append(3, 'Close')
        return menu

    def OnTaskBarClose(self, event):
        """ Close main window """
        self.frame.Destroy()
        self.Destroy()
    def OnTaskBarActivate(self, event):
        """ Shoow window """
        if not self.frame.IsShown():
            self.frame.Show()

    def OnTaskBarDeactivate(self, event):
        """ Hide the window """
        if self.frame.IsShown():
            self.frame.Hide()

if __name__ == "__main__":
    print "This is a module for netspy2ban.py"
