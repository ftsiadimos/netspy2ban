#!/usr/bin/python
""" This is a module for the networking.py"""
# -*- coding: utf-8 -*-
#
# Copyright 2015 Fotios Tsiadimos
# Licensed under the terms of the GPL License
# (see License file for details)

import socket
import glob
import re
import os

PROC_TCP = "/proc/net/tcp"


STATE = {
        '01':'ESTABLISHED',
        '02':'SYN_SENT',
        '03':'SYN_RECV',
        '04':'FIN_WAIT1',
        '05':'FIN_WAIT2',
        '06':'TIME_WAIT',
        '07':'CLOSE',
        '08':'CLOSE_WAIT',
        '09':'LAST_ACK',
        '0A':'LISTEN',
        '0B':'CLOSING'
        }

def _load():
    ''' Read the table of tcp connections & remove header  '''
    with open(PROC_TCP,'r') as f:
        content = f.readlines()
        content.pop(0)
    return content

def _hex2dec(s):
    return str(int(s,16))

def _ip(s):
    ip = [(_hex2dec(s[6:8])),(_hex2dec(s[4:6])),(_hex2dec(s[2:4])),(_hex2dec(s[0:2]))]
    return '.'.join(ip)

def _remove_empty(array):
    return [x for x in array if x !='']

def _convert_ip_port(array):
    host,port = array.split(':')
    return _ip(host),_hex2dec(port)


def _get_pid_of_inode(inode):
    for item in glob.glob('/proc/[0-9]*/fd/[0-9]*'):
        try:
            if re.search(inode,os.readlink(item)):
                return item.split('/')[2]
        except:
            pass
    return None


def netstat():
    """ Main Function """
    listen_ports =[]
    est_ports = []
    content=_load()
    result = {}
    for line in content:
        line_array = _remove_empty(line.split(' '))     # Split lines and remove empty spaces.
        l_host,l_port = _convert_ip_port(line_array[1]) # Convert ipaddress and port from hex to decimal.
        r_host,r_port = _convert_ip_port(line_array[2])
        tcp_id = line_array[0]
        state = STATE[line_array[3]]
        inode = line_array[9]                           # Need the inode to get process pid.
        pid = _get_pid_of_inode(inode)                 # Get pid prom inode.


        try:
            with open('/proc/'+pid+'/status', 'r') as f:
                exe = f.readline().split("\t")[1].rstrip()
        except:
            exe = 'Unknown'

        if state == STATE['0A'] or l_port in est_ports: #LISTEN
            if l_port not in listen_ports:
                listen_ports.append(l_port)
                port = l_port
                l_host = r_host
                r_host = l_host
        else:
            port = r_port

        try:
            service = socket.getservbyport(int(port))
        except:
            service = 'Unknown'

        est_ports.append(port)
        result[tcp_id] = [l_host,r_host,str(port),service, exe, pid]
        
    return result
    
if __name__ == "__main__":
    print "This is a module for netspy2ban.py"
