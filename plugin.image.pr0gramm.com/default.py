#!/usr/bin/python

import sys
import os
import urllib
import urllib2
import urlparse
import re
import xbmc
import xbmcgui
import xbmcplugin

website_url = "http://pr0gramm.com/static/"

base_url = sys.argv[0]
addon_handle = int(sys.argv[1])
args = urlparse.parse_qs(sys.argv[2][1:])

def build_url(query):
    return base_url + '?' + urllib.urlencode(query)

def read_html(url):
   web_sock = urllib.urlopen(url)
   html = web_sock.read()
   web_sock.close()
   return html

def create_dir_item(url):
   list_item = xbmcgui.ListItem(url)
   list_item.setProperty('IsPlayable', 'true')
   xbmcplugin.addDirectoryItem(addon_handle, url, list_item, isFolder=False)

def display_image_num(image_num):
   image_url = website_url + image_num
   image = re.compile('<img src="(http://img.pr0gramm.com/.*?)"', re.IGNORECASE).findall(read_html(image_url))
   for i in image:
      create_dir_item(i)

def display_image_site(url):
   images = re.compile('<a href="/static/([0-9]*)">', re.IGNORECASE).findall(read_html(url))
   for image_num in images:
      display_image_num(image_num)

def get_next_image_site(url):
   next_image_site = re.compile('href="/static/(top/[0-9]+)"', re.IGNORECASE).findall(read_html(url))
   return website_url + next_image_site[0]

def get_next_n_image_sites(n):
   url = website_url
   result = []
   for i in range(0,n):
      result.append(url)
      url = get_next_image_site(url)
   return result

mode = args.get('mode', None)

if mode is None:
   li = xbmcgui.ListItem('Site 1-10')
   url = build_url({'mode': 'image_site', 'n': 10, 'image_site_url': website_url})
   xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)
   i = 1
   for site in get_next_n_image_sites(5):
      li = xbmcgui.ListItem('Site ' + str(i))
      url = build_url({'mode': 'image_site', 'n': 1, 'image_site_url': site})
      xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)
      i = i + 1
elif mode[0] == 'image_site':
   url = args['image_site_url'][0]
   n = args['n'][0]
   for i in range(0,int(n)):
      print i
      display_image_site(url)
      url = get_next_image_site(url)
   li = xbmcgui.ListItem('Next')
   url = build_url({'mode': 'image_site', 'n': n, 'image_site_url': get_next_image_site(url)})
   xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)

xbmcplugin.endOfDirectory(addon_handle)

