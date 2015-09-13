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
          
cheesy gives you the news for today's cheese pipy factory

Usage:
  cheesy (ls | list)
  cheesy [PACKAGE...]
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

__version__ = "0.1.0"


def _pull_all(command):
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

	if command == 'ls':
		for li in l:
			print ">  %s - %s"%(li[0],li[4])
	if command == 'list':
		for li in l:
			name = li[0] + "".join(" " for i in range(name_max-len(li[0])))
			desc = li[1]
			if len(li[1]) > 56:
				desc = desc[:56] + " .."
			print ">  %s - %s"%(name,desc)


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


# under info
def _construct(PACKAGE):
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
	releases_version = "0.2.7" # will be given by input user
	release_point = jsn['releases'][releases_version][0]
	download_url_for_release = release_point['url']
	download_num_for_release = release_point['downloads']
	download_size_for_release = _sizeof_fmt(int(release_point['size']))
	return dict(locals())


def main():
    '''cheesy gives you the news for today's cheese pipy factory from command line'''
    arguments = docopt(__doc__, version=__version__)

    if arguments['ls']:
        pprint(_pull_all('ls'))
    elif arguments['list']:
        pprint(_pull_all('list'))
    elif arguments['PACKAGE']:
    	for package in arguments['PACKAGE']:
    		try:
        		pprint(_construct(package))
        	except ValueError:
        		print "Error: package not found try.. \n$ cheese ls \nto view pacakages"
    else:
        print(__doc__)


if __name__ == '__main__':
	main()