#!/usr/bin/env python
""" Networking Panel """
# -*- coding: utf-8 -*-
# Copyright 2015 Fotios Tsiadimos
# Licensed under the terms of the GPL License
# (see License file for details)

import wx
import socket
import sys
import netstatus
import winmesg

FILE_PATH = '/proc/net/nf_conntrack'

class Networkclass(wx.Panel):
    """Network connections"""
    def __init__(self, parent, idwx=-1):
        """ Initialize the networking panel """
        wx.Panel.__init__(self, parent, idwx)
        mastersizer = wx.BoxSizer(wx.VERTICAL)
        mastersizer.AddSpacer(15)

        txtheader = wx.StaticText(self, -1, 'Networking', (0, 0))
        font = wx.Font(16, wx.DEFAULT, wx.NORMAL, wx.BOLD)
        txtheader.SetFont(font)

        rowtopsizer = wx.BoxSizer(wx.HORIZONTAL)
        rowtopsizer.Add(txtheader, 3, wx.ALIGN_LEFT)
        rowtopsizer.Add((0, 0), 1)
        mastersizer.Add(rowtopsizer, 0,\
            flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=15)

        self.host1 = wx.StaticText(self, -1, "Program")
        self.host2 = wx.StaticText(self, -1, "Pid")
        self.host11 = wx.StaticText(self, -1, "hostname")

        self.tab1 = wx.ListCtrl(self, -1, style=wx.LC_REPORT | wx.LC_VRULES |wx.EXPAND)
        self.tab1.Bind(wx.EVT_LIST_ITEM_SELECTED, self.onitemselected)
        self.tab1.InsertColumn(0, 'Source', width=135)
        self.tab1.InsertColumn(1, 'Destination', width=135)
        self.tab1.InsertColumn(2, 'Port', width=90)
        self.tab1.InsertColumn(3, 'Service', width=276)

        mastersizer.Add(self.tab1, 1, wx.EXPAND)
        wx.EVT_TIMER(self, -1, self._ontimer)
        self.timer = wx.Timer(self, -1)
        self.timer.Start(1000)

        rowbottomsizer = wx.BoxSizer(wx.HORIZONTAL)
        mastersizer.Add(rowbottomsizer, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=15)
        font1 = wx.Font(11, wx.DEFAULT, wx.NORMAL, wx.BOLD)
        self.host1.SetFont(font1)
        self.host2.SetFont(font1)
        self.host11.SetFont(font1)
        newbox = wx.BoxSizer(wx.VERTICAL)
        newbox.Add(self.host11, 1, wx.ALIGN_LEFT)
        newbox.Add(self.host1, 1, wx.LEFT)
        newbox.Add(self.host2, 1, wx.LEFT)
        mastersizer.Add(newbox, 0, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=15)

        mysocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        mysocket.connect(("8.8.8.8", 80))
        self.myhost = (mysocket.getsockname()[0])
        mysocket.close()

        self.SetSizer(mastersizer)
        self.Hide()
        self.cur_view = []
        self.mess = []

    def onitemselected(self, event):
        """mouse click on rows"""
        my_netstat = netstatus.netstat()
        list_split = []
        currentitem = event.m_itemIndex
        for i in  self.cur_view[currentitem]:
            list_split.append(i)
        if self.myhost == list_split[4].lstrip('dst='):
            my_ip = list_split[3].lstrip('scr=')
        else:
            my_ip = list_split[4].lstrip('dst=')
        for tcp_id, details1 in my_netstat.iteritems():
            if my_ip  in details1:
                if details1[4] and details1[5]:
                    nameofprogram = details1[4]
                    pid = details1[5]
                else:
                    nameofprogram = "Unknown"
                    pid = "Unknown"
                break
            else:
                nameofprogram = "Unknown"
        try:
            my_host = socket.gethostbyaddr(my_ip)
            my_host = my_host[0]
        except:
            my_host = 'Unknown'

        self.host11.SetLabel(my_host)
        self.host1.SetLabel(nameofprogram)
        self.host2.SetLabel(pid)

    def _ofile(self):
        """Read file"""
        net_list = []
        try:
            with open(FILE_PATH) as n_list:
                for i in n_list:
                    list_split = i.split()
                    if list_split[2] == "tcp":
                        del list_split[0:3]
                        por = list_split[6]
                        por = por.lstrip('dport=')
                        try:
                            service = socket.getservbyport(int(por))
                        except:
                            service = 'Unknown'
                        list_split[1] = service
                        del list_split[7:]
                        del list_split[5]
                        net_list.append(list_split)
            return net_list
        except IOError:
            error_msg = "Didn't find nf_contrack in /proc/net folder."
            print error_msg
            self.showerror(self, error_msg)


    def _ontimer(self, event):
        """ Refresh and show network card details."""
        cur_netstat = self._ofile()
        cur_netstat.sort()
        self.tab1.Freeze()
        j = 0
        for details in  self.cur_view:
            if details not in cur_netstat:
                del self.cur_view[j]
                self.tab1.DeleteItem(j)
            j += 1
        for details in cur_netstat:
            if details not in self.cur_view:
                if details[2] == "ESTABLISHED":
                    if "127.0.0.1" not in details[3]:
                        i = self.tab1.InsertStringItem(sys.maxint, str(details[0]))
                        self.tab1.SetStringItem(i, 0, details[3].lstrip('scr='))
                        self.tab1.SetStringItem(i, 1, details[4].lstrip('dst='))
                        self.tab1.SetStringItem(i, 2, details[5].lstrip('dport='))
                        self.tab1.SetStringItem(i, 3, details[1])
                        self.cur_view.append(details)
                        if self.myhost != details[3].lstrip('scr='):
                            source = details[3].lstrip('scr=')
                            port = details[5].lstrip('dport=')
                            winmesg.toster(self, \
         "Server {0} is trying to connect via port {1}".format(source, port))
        count_rows = self.tab1.GetItemCount()
        for row in range(count_rows):
            if row % 2:
                self.tab1.SetItemBackgroundColour(row, "#FFFFFF")
            else:
                self.tab1.SetItemBackgroundColour(row, "#E5E5E5")
                self.tab1.SetBackgroundStyle(wx.LC_HRULES)
        self.tab1.Thaw()

    def showerror(self, event, error_msg):
        """ Popup message error """
        dial = wx.MessageDialog(None, error_msg, 'Error', \
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
