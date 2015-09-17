#!/usr/bin/env python
# -*- coding: utf-8 -*-
r"""
           ▄▄                                               
           ██                                               
  ▄█████▄  ██▄████▄   ▄████▄    ▄████▄   ▄▄█████▄  ▀██  ███ 
 ██▀    ▀  ██▀   ██  ██▄▄▄▄██  ██▄▄▄▄██  ██▄▄▄▄ ▀   ██▄ ██  
 ██        ██    ██  ██▀▀▀▀▀▀  ██▀▀▀▀▀▀   ▀▀▀▀██▄    ████▀  
 ▀██▄▄▄▄█  ██    ██  ▀██▄▄▄▄█  ▀██▄▄▄▄█  █▄▄▄▄▄██     ███   
   ▀▀▀▀▀   ▀▀    ▀▀    ▀▀▀▀▀     ▀▀▀▀▀    ▀▀▀▀▀▀      ██    
                                                    ███     
          
cheesy gives you the news for today's cheese shop pipy factory

Usage:
  cheesy (ls | list)
  cheesy <PACKAGE> 
  cheesy <PACKAGE> <VERSION>
  cheesy (-h | --help)
  cheesy --version

Options:
  -h --help     Show this screen.
  --version     Show version.
"""



import requests
from bs4 import BeautifulSoup
import urlparse
BASE_URL = "https://pypi.python.org/pypi"
from docopt import docopt
from pprint import pprint
import cheesy
__version__ = cheesy.__version__


import logging
logging.captureWarnings(True)


def _pull_all(command):
	"""Website scraper for the info from table content"""
	page = requests.get(BASE_URL,verify=False)
	soup = BeautifulSoup(page.text,"lxml")
	table = soup.find('table',{'class':'list'})
	rows = table.findAll("tr")
	rows = rows[1:-1]
	l = []
	name_max = 0

	for row in rows:
		elements = row.findAll('td')
		date = elements[0].string
		name = elements[1].string
		n = _ascii_checker(name)
		version = n.split(' ')[1]
		name = n.split(' ')[0]
		if name_max < len(name):
			name_max = len(name)
		link = elements[1].find('a')['href']
		link = urlparse.urljoin(BASE_URL,link)
		desc = elements[2].string
		li = (name,desc,link,date,version)
		l.append(li)

	print u"\n\033[1m\033[1m\033[4m PACKAGES \033[0m\n"
	if command == 'ls':
		for li in l:
			print u"\033[1m \u25E6 %s \033[0m - \033[93m%s \033[0m"%(li[0],li[4])
	if command == 'list':
		for li in l:
			name = li[0] + "".join(" " for i in range(name_max-len(li[0])))
			desc = li[1]
			if len(li[1]) > 56:
				desc = desc[:56] + " .."
			print u"\033[1m \u25D8  %s \033[0m - \033[93m%s \033[0m"%(name,desc)


def _ascii_checker(name):
	return "".join([[ch," "][ord(ch) > 128] for ch in name ])


def _get_info(package_name):
	return requests.get("https://pypi.python.org/pypi/{}/json".format(package_name),verify=False).json()


def _sizeof_fmt(num, suffix='B'):
    for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)


def _release_info(jsn,VERSION):
	"""Gives information about a particular package version."""
	try:
		release_point = jsn['releases'][VERSION][0]
	except KeyError:
		print "\033[91m\033[1mError: Release not found."
		exit(1)
	python_version = release_point['python_version']
	filename = release_point['filename']
	md5 = release_point['md5_digest']
	download_url_for_release = release_point['url']
	download_num_for_release = release_point['downloads']
	download_size_for_release = _sizeof_fmt(int(release_point['size']))
	print """
	\033[1m\033[1m        \033[4mPACKAGE VERSION INFO\033[0m

	\033[1m	md5                  :\033[0m   \033[93m%s  \033[0m
	\033[1m	python version       :\033[0m   \033[93m%s  \033[0m	
	\033[1m	download url         :\033[0m   \033[93m%s  \033[0m	
	\033[1m	download number      :\033[0m   \033[93m%s  \033[0m
	\033[1m	size                 :\033[0m   \033[93m%s  \033[0m	
	\033[1m	filename             :\033[0m   \033[93m%s  \033[0m	
	"""%(md5,python_version,download_url_for_release,\
	     download_num_for_release,download_size_for_release,filename)

def _construct(PACKAGE,VERSION):
	"""Construct the information part from the API."""
	jsn  = _get_info(PACKAGE)
	package_url = jsn['info']['package_url']
	author = jsn['info']['author']
	author_email = jsn['info']['author_email']
	description = jsn['info']['description'] 
	last_month = jsn['info']['downloads']['last_month']
	last_week = jsn['info']['downloads']['last_week']
	last_day = jsn['info']['downloads']['last_day']
	classifiers = jsn['info']['classifiers']
	license = jsn['info']['license']
	summary = jsn['info']['summary']
	home_page = jsn['info']['home_page']
	releases = jsn['releases'].keys()
	releases = ' | '.join(releases)[:56]
	download_url = jsn['urls'][0]['url']
	filename = jsn['urls'][0]['filename']
	size = _sizeof_fmt(int(jsn['urls'][0]['size']))
	
	if VERSION:
		_release_info(jsn,VERSION)
		return None

	print """
	\n\033[1m\033[4mDESCRIPTION\n\n\033[0m\033[93m%s  \033[0m
	
	\033[1m\033[1m        \033[4mPACKAGE INFO\033[0m

	\035[1m	package url          :\033[0m   \033[93m%s  \033[0m
	\033[1m	author name          :\033[0m   \033[93m%s  \033[0m
	\033[1m	author email         :\033[0m   \033[93m%s  \033[0m
	\033[1m	downloads last month :\033[0m   \033[93m%s  \033[0m
	\033[1m	downloads last week  :\033[0m   \033[93m%s  \033[0m
	\033[1m	downloads last day   :\033[0m   \033[93m%s  \033[0m
	\033[1m	homepage             :\033[0m   \033[93m%s  \033[0m
	\033[1m	releases             :\033[0m   \033[93m%s  \033[0m	
	\033[1m	download url         :\033[0m   \033[93m%s  \033[0m	
	\033[1m	filename             :\033[0m   \033[93m%s  \033[0m	
	\033[1m	size                 :\033[0m   \033[93m%s  \033[0m	
	"""%(description,package_url,author,author_email,last_month,last_week,\
	     last_day,home_page,releases,download_url,filename,size)


def main():
    '''cheesy gives you the news for today's cheese pipy factory from command line'''
    arguments = docopt(__doc__, version=__version__)
    if arguments['ls']:
        _pull_all('ls')
    elif arguments['list']:
        _pull_all('list')
    elif arguments['<PACKAGE>']:
		try:
			if arguments['<VERSION>']:
				_construct(arguments['<PACKAGE>'],arguments['<VERSION>'])
			else:
				_construct(arguments['<PACKAGE>'],None)
		except ValueError:
			print "\033[91m\033[1mError: package not found try.. \033[0m\033[1m\n$ cheese ls \nto view pacakages"
    else:
        print(__doc__)


if __name__ == '__main__':
	main()