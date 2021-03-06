#!/usr/bin/env python
""" Fail2ban Gui controler"""
# -*- coding: utf-8 -*-
# Copyright 2015 Fotios Tsiadimos
# Licensed under the terms of the GPL License
# (see License file for details)

import wx
import sys
import ConfigParser
import os
import shutil
import subprocess
import fileinput
import commands
import winmesg
from datetime import datetime

FILE_PATH = '/var/log/fail2ban.log'
JAIL_PATH = '/etc/fail2ban/jail.local'

class Fail2banclass(wx.Panel):
    """GUI control and logs for fail2ban"""
    def __init__(self, parent, idwx=-1):
        if not os.path.isfile(JAIL_PATH):
            shutil.copy2('/etc/fail2ban/jail.conf', JAIL_PATH)
            for line in fileinput.input(JAIL_PATH, inplace=1):
                if "auto" in line:
                    line = line.replace("backend = auto", "backend = systemd")
                sys.stdout.write(line)
            command = ['/usr/sbin/service', 'fail2ban', 'restart']
            subprocess.call(command, shell=False)

        wx.Panel.__init__(self, parent, idwx)
        out = commands.getoutput('ps -A')

        self.parser = ConfigParser.ConfigParser()
        self.parser.read(JAIL_PATH)
        distros = self.parser.sections()
        for i in distros:
            if i not in out:
                self.parser.set(i, 'enabled', 'false')
        if 'INCLUDES' in distros:
            distros.remove('INCLUDES')

        sshcheck = self.parser.getboolean('sshd', 'enabled')
        sshmaxtry = self.parser.getint('sshd', 'maxretry')
        banti = self.parser.getint('DEFAULT', 'bantime')
        findti = self.parser.getint('DEFAULT', 'findtime')

        mastersizer = wx.BoxSizer(wx.VERTICAL)
        mastersizer.AddSpacer(15)
        self.box = wx.CheckBox(self, label='sshd')
        self.box.Bind(wx.EVT_CHECKBOX, self.checkboxf)

        self.box.SetValue(sshcheck)
        lab1 = wx.StaticText(self, 1, "Ban-time:")
        self.box1 = wx.SpinCtrl(self, value='1', size=(1, -1), min=1, max=12000)
        self.box1.SetValue(banti)
        lab2 = wx.StaticText(self, 1, "Find-time:")
        self.box2 = wx.SpinCtrl(self, value='1', size=(1, -1), min=1, max=12000)
        self.box2.SetValue(findti)
        lab3 = wx.StaticText(self, 1, "Ban-after:")
        self.box3 = wx.SpinCtrl(self, value='1', size=(1, -1), min=1, max=12)
        self.box3.SetValue(sshmaxtry-1)
        butapply = wx.Button(self, label='Apply', pos=(550, 15))
        butapply.Bind(wx.EVT_BUTTON, self.applybutton)

        combox = wx.ComboBox(self, choices=distros, style=wx.CB_READONLY)
        combox.SetSelection(0)
        combox.Bind(wx.EVT_COMBOBOX, self.onselect)

        txtheader = wx.StaticText(self, -1, 'Fail2Ban', (0, 0))
        font = wx.Font(16, wx.DEFAULT, wx.NORMAL, wx.BOLD)
        font1 = wx.Font(10, wx.NORMAL, wx.NORMAL, wx.NORMAL)
        txtheader.SetFont(font)
        self.box.SetFont(font1)
        lab1.SetFont(font1)
        lab2.SetFont(font1)
        lab3.SetFont(font1)
        rowtopsizer = wx.BoxSizer(wx.HORIZONTAL)
        rowtopsizer.Add(txtheader, 3, wx.ALIGN_LEFT)
        rowtopsizer.Add((0, 0), 1)

        mastersizer.Add(rowtopsizer, 0, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=15)

        self.sizerv = wx.StaticBoxSizer(wx.StaticBox(self, wx.NewId(), \
             'General Settings'), wx.HORIZONTAL)
        self.sizerva = wx.StaticBoxSizer(wx.StaticBox(self, wx.NewId(), \
             'Services Settings'), wx.HORIZONTAL)
        self.sizerv.Add(lab1, 0, wx.CENTER)
        self.sizerv.Add(self.box1, 1)
        self.sizerv.Add(lab2, 0, wx.CENTER)
        self.sizerv.Add(self.box2, 1)
        self.sizerva.Add(self.box, 1, wx.CENTER)
        self.sizerva.Add(combox, 1)
        self.sizerva.Add(lab3, 0, wx.CENTER)
        self.sizerva.Add(self.box3, 1)
        mastersizer.Add(self.sizerv, 0, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=5)
        mastersizer.Add(self.sizerva, 0, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=5)
        self.tab1 = wx.ListCtrl(self, -1, style=wx.LC_REPORT | wx.LC_VRULES | wx.EXPAND)

        self.tab1.InsertColumn(0, 'Date', width=120)
        self.tab1.InsertColumn(1, 'Time', width=95)
        self.tab1.InsertColumn(2, 'Port', width=100)
        self.tab1.InsertColumn(3, 'Source', width=140)
        self.tab1.InsertColumn(4, 'Ban/Unban', width=180)

        mastersizer.Add(self.tab1, 1, wx.EXPAND)

        wx.EVT_TIMER(self, -1, self._ontimer)

        self.timer = wx.Timer(self, -1)
        self.timer.Start(1000)

        rowbottomsizer = wx.BoxSizer(wx.HORIZONTAL)

        mastersizer.Add(rowbottomsizer, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=15)

        mastersizer.AddSpacer(15)
        self.SetSizer(mastersizer)
        self.cur_view = []
        self.Hide()
        self.service = " "

    def applybutton(self, event):
        """ Save the changes inthe configure file """

        banv = self.box1.GetValue()
        findv = self.box2.GetValue()
        maxv = self.box3.GetValue()
        self.parser.set('DEFAULT', 'bantime', banv)
        self.parser.set('DEFAULT', 'findtime', findv)
        if self.service == " ":
            self.parser.set("sshd", 'maxretry', maxv+1)
        else:
            self.parser.set(self.service, 'maxretry', maxv+1)
        with open(JAIL_PATH, 'wb') as configfile:
            self.parser.write(configfile)

        command = ['/usr/bin/fail2ban-client', 'reload']
        subprocess.call(command, shell=False)

    def checkboxf(self, event):
        """ Enable/Disabe the services """
        out = commands.getoutput('ps -A')
        if self.service == " ":
            self.service = "sshd"
        if self.service in out:
            sender = event.GetEventObject()
            ischecked = sender.GetValue()
            if ischecked:
                self.parser.set(self.service, 'enabled', 'true')
            else:
                self.parser.set(self.service, 'enabled', 'false')

            with open(JAIL_PATH, 'wb') as configfile:
                self.parser.write(configfile)
        else:
            self.showrror(self, \
            "ERROR: The service is not enabled, please check that it is running.", exit=1)
            self.box.SetValue(False)

    def onselect(self, event):
        """ SpinCtrl checking """

        self.service = event.GetString()
        sshcheck = self.parser.getboolean(self.service, 'enabled')
        self.box.SetValue(sshcheck)
        font3 = wx.Font(10, wx.NORMAL, wx.NORMAL, wx.NORMAL)
        try:
            self.box3.SetRange(1, 12)
            sshmaxtry = self.parser.getint(self.service, 'maxretry')
            self.box3.SetValue(sshmaxtry-1)
        except:
            self.box3.SetRange(1, 0)
        self.box.SetLabel(self.service)
        self.box.SetFont(font3)

    def showrror(self, event, error_msg, exit):
        """ Mesg Error Box """
        dial = wx.MessageDialog(None, error_msg, 'Error', wx.OK | wx.ICON_ERROR)
        dial.ShowModal()
        if exit != 1:
            sys.exit()

    def openfile(self):
        """ Reading the log file """
        try:
            ban = ['Ban', 'Unban']
            filelist = []
            items = open(FILE_PATH)
            for item in items:
                if  "NOTICE"  in item:
                    splitv = item.split()
                    for i in splitv:
                        if i in ban:
                            filelist.append(splitv)
            items.close()
            return filelist
        except IOError:
            error_msg = "You need to activate the fail2ban.log file in your /var/log folder."
            print error_msg
            self.showrror(self, error_msg, 0)

    def _ontimer(self, event):
        """Refresh log messages."""

        listfile = self.openfile()
        for i in listfile:
            date = str(i[0])
            time = str(i[1])
            time = time[:-4]
            port = str(i[5])
            port = port.replace('[', '').replace(']', '')
            source = str(i[6])
            ban = str(i[7])

            if i not in self.cur_view:
                index = 0
                self.tab1.InsertStringItem(index, date)
                self.tab1.SetStringItem(index, 1, time)
                self.tab1.SetStringItem(index, 2, port)
                self.tab1.SetStringItem(index, 3, ban)
                self.tab1.SetStringItem(index, 4, source)
                self.cur_view.append(i)
                index -= 1
                cur_time = str(datetime.now().time())
                cur_time = cur_time.split(".")[0]
                cur_time = cur_time[:-1]
                timeix = time[:-1]
                if cur_time in timeix:
                    if source == 'Ban':
                        source = "banned"
                    else:
                        source = "unbanned"
                    winmesg.toster(self, 'Server {0} is {1}'.format(ban, source))
            count_rows = self.tab1.GetItemCount()
            for row in range(count_rows):
                if row % 2:
                    self.tab1.SetItemBackgroundColour(row, "#FFFFFF")
                else:
                    self.tab1.SetItemBackgroundColour(row, "#E5E5E5")
                    self.tab1.SetBackgroundStyle(wx.LC_HRULES)

    def showyourself(self):
        """Shows the panel on the main frame."""
        self.Raise()
        self.SetPosition((0, 0))
        self.Fit()
        self.GetParent().GetSizer().Show(self)
        self.GetParent().GetSizer().Layout()

if __name__ == "__main__":
    print "This is a module for netspy2ban.py"
