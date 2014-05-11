#! /usr/bin/env python
# -*- coding: utf-8 -*- 
# coding=utf-8

# use httplib2 sample,need single install httplib2
'''
from httplib2 import Http
from urllib import urlencode
h = Http()
data = dict(username="useradmin", password="725fa")
resp, content = h.request("http://192.168.1.1/ctlogin.cmd", "POST", urlencode(data))
resp
'''

import os
import sys
import subprocess
import time
import urllib, urllib2, cookielib
import re


from time import gmtime, strftime
def getTime():
        return strftime("%Y-%m-%d %H:%M:%S", gmtime())

username = 'useradmin'
password = '725fa'

def restartRouter():
        try:
                cj = cookielib.CookieJar()
                opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
                login_data = urllib.urlencode({'username' : username, 'j_password' : password})
                resp = opener.open('http://192.168.1.1/ctlogin.cmd', login_data)
                #resp = opener.open('http://192.168.1.1/ctinfo.html')
                #resp = opener.open('http://192.168.1.1/ctlogout.cmd')
                resp = opener.open('http://192.168.1.1/resetrouter.html')
                html = resp.read()

                #print html
                #print '---------------------'
                #m = re.match(r"sessionKey='(\d+)';",html)
                #m = re.match(r".*sessionKey='(\d+)'\S*",html)
                #m = re.match(r".*\s*.*sessionKey='(\d+)'.*",html)
                m = re.match(r"[.*\s*\S*]*sessionKey='(\d+)'",html)
                if m:
                        #print m.group(1)
                        print 'restart router,please wait 120s. ' + getTime()
                        resp = opener.open('http://192.168.1.1/rebootinfo.cgi?sessionKey=' + m.group(1))
                        sleep(120)
                        #print resp.read()
                        
                else:
                        print 'error: can not find session key! ' + getTime()
                        resp = opener.open('http://192.168.1.1/ctlogout.cmd')
        except:
                print 'router error! please wait 120s.' + getTime()
                sleep(120)
        
def check():
        d = 0
        while True:
                
                host = 'qq.com'
                p = subprocess.Popen(" ping -n 1 -w 2 "+ host,
                        stdin = subprocess.PIPE,
                        stdout = subprocess.PIPE,
                        stderr = subprocess.PIPE,
                        shell = True)
                out = p.stdout.read()
                regex = re.compile("TTL=\d*", re.IGNORECASE | re.MULTILINE)
                if len(regex.findall(out)) > 0:
                        print 'Router internet is OK! ' + getTime()
                        print ''
                        d = 0
                else:
                        print str(d) + ' Router internet down! Please check it! ' + getTime()
                        print "\a"
                        d += 1
                if d > 5:
                        d = 0
                        restartRouter()
                time.sleep(20)
                
if __name__ == "__main__":
        check()
                
                
                
                
