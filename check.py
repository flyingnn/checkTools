#! /usr/bin/env python
# -*- coding: utf-8 -*- 
# coding=utf-8

import os
import sys
import re
import subprocess
import time

from ctypes import *
import win32con

import win32gui as w
cur_window = w.GetForegroundWindow() #just get the handler/ID for the current window

__all__ = ['flash']

FlashWindowEx = windll.user32.FlashWindowEx

class FLASHWINFO(Structure):
        _fields_ = [('cbSize', c_uint),
                ('hwnd', c_uint),
                ('dwFlags', c_uint),
                ('uCount', c_uint),
                ('dwTimeout', c_uint)]
    
def flash(hwnd):
        '''Flash a window with caption and tray.'''
        info = FLASHWINFO(0, hwnd, win32con.FLASHW_ALL | win32con.FLASHW_TIMERNOFG, 0, 0)
        info.cbSize = sizeof(info)
        FlashWindowEx(byref(info))
    
    
def check(hosts):
        d = {}
        while True:
                file = open(hosts)
                for host in file.readlines():
                        host = host.strip('\n')
                        if not d.has_key(host):
                                d[host] = 0
                        p = subprocess.Popen(" ping -n 1 -w 2 "+ host,
                                stdin = subprocess.PIPE,
                                stdout = subprocess.PIPE,
                                stderr = subprocess.PIPE,
                                shell = True)
                        out = p.stdout.read()
                        regex = re.compile("TTL=\d*", re.IGNORECASE | re.MULTILINE)
                        if len(regex.findall(out)) > 0:
                                print host+': Up! It is OK!'
                                d[host] = 0
                                print ''
                        else:
                                d[host] += 1
                                print host+': Down! Please check it!'
                                print ''
                                if d[host] > 1:
                                        print "\a"
                                        flash(cur_window)
                                        d[host] =0
                time.sleep(5)

if __name__ == "__main__":
        if os.path.exists('hosts.txt'): 
                check('hosts.txt')
        else:
                print "not found file: hosts.txt"