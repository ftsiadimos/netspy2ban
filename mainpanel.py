#!/usr/bin/env python 
""" First Networking Panel """
# -*- coding: utf-8 -*-
#
# Copyright 2015 Fotios Tsiadimos
# Licensed under the terms of the GPL License
# (see License file for details)

import wx
import time
import platform
import sys
from datetime import timedelta

FILE_PATH = '/proc/net/dev'
UPTIME_PATH = '/proc/uptime'

class Main_Class(wx.Panel):
    """Netwok cards."""
    def __init__(self, parent, idwx= -1):

        wx.Panel.__init__(self, parent, idwx)
        
        self.lasttime = 1
        self.lastbin = [0]
        self.lastbout = [0]
        self.speedin = [0]
        self.speedout = [0]
       
        unames = platform.uname()
        self.host0 = wx.StaticText(self, -1,'time', (5, 250))
        self.host1 = wx.StaticText(self, -1, unames[0], (5, 270)) 
        self.host2 = wx.StaticText(self, -1, unames[1], (5, 290)) 
        self.host3 = wx.StaticText(self, -1, unames[2], (5, 310)) 
                
        wx.EVT_TIMER(self, -1, self.ontimer)

        self.timer = wx.Timer(self, -1)
        self.timer.Start(1000) 
        
        txtheader = wx.StaticText(self, -1, 'Status', (0, 0))
        font = wx.Font(16, wx.DEFAULT, wx.NORMAL, wx.BOLD)
        font1 = wx.Font(11, wx.DEFAULT, wx.NORMAL, wx.BOLD)
        txtheader.SetFont(font)  
        self.host2.SetFont(font1)
        self.host3.SetFont(font1)
        self.host1.SetFont(font1)
        self.host0.SetFont(font1)
            
        sizer = wx.BoxSizer(wx.VERTICAL)
     
        sizer.AddSpacer(15)
        sizer.Add(txtheader, 0, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=15) 
                
        self.tab1 = wx.ListCtrl(self, 0, style=wx.LC_REPORT, pos=(3, 3), size=(250, 200))
        self.tab1.InsertColumn(0, 'Device', wx.LIST_FORMAT_CENTER, width=100)
        self.tab1.InsertColumn(1, 'Received MB', wx.LIST_FORMAT_CENTER, width=130)
        self.tab1.InsertColumn(2, 'Sent MB', wx.LIST_FORMAT_CENTER, width=130)
        self.tab1.InsertColumn(3, 'Download KB/s', wx.LIST_FORMAT_CENTER, width=120)
        self.tab1.InsertColumn(4, 'Uploaad KB/s', wx.LIST_FORMAT_CENTER, width=120)
        #self.tab1.SetBackgroundColour("#F2F1F0")
        sizer.Add(self.tab1, 0,  wx.EXPAND) 
      
        self.SetSizer(sizer)  
    def uptime(self):
	with open(UPTIME_PATH) as f:
		uptime_seconds = float(f.readline().split()[0])
		z = str(timedelta(seconds = uptime_seconds))
		z =  z.split('.')
	return z[0]
    def ontimer(self, event):
        """ Refresh and show network card details."""
        net_list = []
        a = str(self.uptime())
        self.host0.SetLabel('Uptime ' + a )
        try:
            with open(FILE_PATH) as demo:    
                self.tab1.Freeze() 
                self.tab1.DeleteAllItems()
                for i in demo:
                    list_split = i.split()
                    if list_split[2] is not  '0':
                        net_list.append(list_split)
                del net_list[0:2]
                net_count = 0          
                timedelta = time.time() - self.lasttime
                self.lasttime = time.time()
                for listrow in net_list:          
    
                    bbin = int(listrow[1])
                    bout = int(listrow[9])
                    
                    self.speedin[net_count] = round((bbin-int(self.lastbin[net_count]))/(1024*timedelta), 2)                   
                    self.speedout[net_count] = round((bout-int(self.lastbout[net_count]))/(1024*timedelta), 2)
                        
                    self.lastbin[net_count] = bbin
                    self.lastbout[net_count] = bout
    
                    download = str(round(float(bbin /1024) / (1024), 2))               
                    upload = str(round(float(bout /1024) / (1024), 2))
        
                    i = self.tab1.InsertStringItem(sys.maxint, str(listrow[0]))
                    self.tab1.SetStringItem(i, 1, download)
                    self.tab1.SetStringItem(i, 2, upload)
                    self.tab1.SetStringItem(i, 3, str(self.speedin[net_count]))
                    self.tab1.SetStringItem(i, 4, str(self.speedout[net_count]))
                    net_count += 1
                    self.lastbin.extend([net_count])
                    self.lastbout.extend([net_count])
                    self.speedin.extend([net_count])
                    self.speedout.extend([net_count])
                    
            self.tab1.Thaw()
        except IOError:
            error_msg =  "Didn't find dev in /proc/net folder."
            print error_msg
            self.ShowError(self, error_msg)
            
    def ShowError(self, event, error_msg):
        dial = wx.MessageDialog(None, error_msg, 'Error', 
            wx.OK | wx.ICON_ERROR)
        dial.ShowModal()
        sys.exit()

    def showyourself(self):
        """Shows the panel on the main frame."""
        self.Raise()
        self.SetPosition((0, 0))
        self.Fit()
        self.GetParent().GetSizer().Show(self)
        self.GetParent().GetSizer().Layout()

if __name__ == "__main__":
    print "This is a module for netspy2ban.py"
