#!/usr/bin/python

import os, sys
import urllib, urllib2, re
import xbmc, xbmcgui, xbmcplugin

base_url = "http://pr0gramm.com/static/"
plugin_handle = int(sys.argv[1])

def readHTML(url):
   WebSock = urllib.urlopen(url)
   WebHTML = WebSock.read()
   WebSock.close()
   return WebHTML

def create_dir_item(url):
   listitem = xbmcgui.ListItem(url)
   listitem.setProperty('IsPlayable', 'true')
   xbmcplugin.addDirectoryItem(plugin_handle, url, listitem, isFolder=False)

def display_image_num(image_num):
   image_url = base_url + image_num
   praefix = "http://img.pr0gramm.com/"
   image = re.compile('<img src="(' + praefix + '.*?)"', re.IGNORECASE).findall(readHTML(image_url))
   for i in image:
      create_dir_item(i)

images = re.compile('<a href="/static/([0-9]*)">', re.IGNORECASE).findall(readHTML(base_url))
for image_num in images:
   display_image_num(image_num)

xbmcplugin.endOfDirectory(plugin_handle)
