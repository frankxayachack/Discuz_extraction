#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = "Sengxay Xayachack"

#require addition module : BeautifulSoup
#installation: pip install beautifulsoup4

import urllib2,re,csv,urllib,cookielib
from bs4 import BeautifulSoup


forumUrl = 'http://laozaa.com'
userName = '##' # USER
password = '##' #PASS
isLogon = False
proxy = None
jar = cookielib.CookieJar()
if not proxy:
    openner = urllib2.build_opener(urllib2.HTTPCookieProcessor(jar))
else:
    openner = urllib2.build_opener(urllib2.HTTPCookieProcessor(jar), urllib2.ProxyHandler({'http' : proxy}))
urllib2.install_opener(openner)

url = forumUrl + "/member.php?mod=logging&action=login&loginsubmit=yes&infloat=yes&inajax=1";
postData = urllib.urlencode({'username': userName, 'password': password, 'answer': '', 'cookietime': '2592000', 'handlekey': 'ls', 'questionid': '0', 'quickforward': 'yes',  'fastloginfield': 'username'})
req = urllib2.Request(url,postData)
content = urllib2.urlopen(req).read()
if userName in content:
    isLogon = True
    print 'login success!'
else:
    print 'login failed!'

def extract_content(post_url):
	data = urllib2.urlopen(post_url).read()
	pid = re.findall('<td class="t_f" id="postmessage_([0-9]+)">' , data) #id
	pid = pid[0] #id
	data = BeautifulSoup(data.decode('utf-8','ignore'))
	content_title = data.title.string
	content_title = content_title.replace(' -  Lao IT Community Laozaa.com -  ','')
	data = data.find("td", {"id":"postmessage_"+pid}) #content
	data = str(data)
	data = data.replace('[hide]','')
	data = data.replace('[/hide]','')
	data = '\n'.join(data.split('\n')[1:]) #cut 1st line
	with open('laozaa.csv', 'a') as csvfile:
		fieldnames = ["author", "content","title"]
		writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
		writer.writeheader()
		writer.writerow({'author':'Devsudsud', 'content':data,'title':content_title.encode('utf-8')})

def extract_topic(category_url):
	#count pages number
	pg_no = 0
	data = urllib2.urlopen(category_url).read()
	webpage_soup = BeautifulSoup(data)
	num = webpage_soup.find('div',{'class':'pg'})
	num = re.findall('(?<=page=)[0-9]+',str(num))
	if num:
		num.pop()
		num.append(1)
		num.sort()
	else:
		num = ['1']
	#END

	######## Extract topics
	category_url = category_url+"&page="
	a = []
	page_no = 1
	for p in range(len(num)):
		a.append(category_url+str(p+1))
	for link in a:
#		print link
		data = urllib2.urlopen(link).read()
		webpage_soup = BeautifulSoup(data)
		print "#################################"
		print "Page : "+str(page_no)+"/"+str(len(num))
		print "#################################"
		thread_table = webpage_soup.find('table', {'id':'threadlisttableid'})
		topic_no = re.findall('(?<=<tbody id="normalthread_)([0-9]+)',str(thread_table))
		print "############TOPICs#############"
		for c in topic_no:
			extract_content("http://laozaa.com/forum.php?mod=viewthread&tid="+str(c)+"&extra=page=1")
			print "ADDED : http://laozaa.com/forum.php?mod=viewthread&tid="+str(c)
		print "#################################"
		page_no += 1

category_url = raw_input("Category URL : ")
extract_topic(category_url)