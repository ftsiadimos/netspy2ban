#!/usr/bin/env python
"""  Taskbar """
# -*- coding: utf-8 -*-
#
# Copyright 2015 Fotios Tsiadimos
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 3, as published
# by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranties of
# MERCHANTABILITY, SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR
# PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.

import wx

class MyTaskBarIcon(wx.TaskBarIcon):
    """Create taskbar"""
    def __init__(self, frame):
        wx.TaskBarIcon.__init__(self)

        self.frame = frame
        self.SetIcon(wx.Icon("/usr/local/bin/icons/netspy2ban.ico", wx.BITMAP_TYPE_ICO), 'NetSpy2Ban')
        self.Bind(wx.EVT_MENU, self.OnTaskBarActivate, id=1)
        self.Bind(wx.EVT_MENU, self.OnTaskBarDeactivate, id=2)
        self.Bind(wx.EVT_MENU, self.OnTaskBarClose, id=3)
        self.Bind(wx.EVT_TASKBAR_LEFT_DOWN, self.on_left_down)

    def on_left_down(self, event):
        if self.frame.IsShown():
            self.frame.Hide()
        else:
            self.frame.Show() 
    def CreatePopupMenu(self):
        menu = wx.Menu()
        menu.Append(1, 'Show')
        menu.Append(2, 'Hide')
        menu.Append(3, 'Close')
        return menu

    def OnTaskBarClose(self, event):
        self.frame.Destroy()
        self.Destroy()
    def OnTaskBarActivate(self, event):
        if not self.frame.IsShown():
            self.frame.Show()

    def OnTaskBarDeactivate(self, event):
        if self.frame.IsShown():
            self.frame.Hide()
  
if __name__ == "__main__":
    print "This is a module for netspy2ban.py"
