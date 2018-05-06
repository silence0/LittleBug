#coding=utf-8
from datetime import *
import time
import os
from splinter import Browser
import re

url = 'http://epub.cnki.net/kns/brief/result.aspx?dbPrefix=CCND'
# 请修改起始和截至日期


cote = [u"人民"]
# 请修改关键词

browser = Browser('chrome')
browser.visit(url)
time.sleep(2)

for conten in cote:
	contentx = conten
	date1 = date(2002,11,8)
	date2 = date(2003,1,7)
	d1 = date(2015,11,22)
	d2 = date(2016,1,21)
	twomouth = d2 - d1
	d3 = date(2016,9,12)

	f1 = open(contentx + '.txt','a')

	
	while (date1 < d3):

		date1s = date1.strftime('%Y-%m-%d')
		date2s = date2.strftime('%Y-%m-%d')

		date1 = twomouth + date1
		date2 = twomouth + date2

		# browser.select("txt_1_sel", "FT") #全文
		browser.find_by_id('txt_1_value1').fill(contentx)
		browser.find_by_id('publishdate_from').fill(date1s)
		browser.find_by_id('publishdate_to').fill(date2s)
		browser.find_by_id('btnSearch').click()
		time.sleep(4)
		div = browser.find_by_id('Show0')
		while (hasattr(div,'html') == False):

			browser.find_by_id('btnSearch').click()
			time.sleep(5)
			div = browser.find_by_id('Show0')

		divh = div.html
		p = re.compile(r'[1-9]\d*\)</span>')
		ns = p.findall(divh)

		f1.write(date1s + "~" + date2s + ":")

		while (ns == "[]"):
			browser.find_by_id('btnSearch').click()
			time.sleep(4)
			div = browser.find_by_id('Show0')

			divh = div.html
			p = re.compile(r'[1-9]\d*\)</span>')
			ns = p.findall(divh)

		for nss in ns:
			nsss = nss[:-8]
			f1.write(nsss + " ")
			print nsss
		f1.write("\n")

	f1.close()

for conten in cote:
	contentx = conten
	date1 = date(2002,11,8)
	date2 = date(2003,1,7)
	d1 = date(2015,11,22)
	d2 = date(2016,1,21)
	twomouth = d2 - d1
	d3 = date(2016,9,12)

	f1 = open(contentx + '2.txt','a')

	
	while (date1 < d3):

		date1s = date1.strftime('%Y-%m-%d')
		date2s = date2.strftime('%Y-%m-%d')

		date1 = twomouth + date1
		date2 = twomouth + date2

		# browser.select("txt_1_sel", "FT") 
		browser.find_by_id('txt_1_value1').fill(contentx)
		browser.find_by_id('publishdate_from').fill(date1s)
		browser.find_by_id('publishdate_to').fill(date2s)
		browser.find_by_id('btnSearch').click()
		time.sleep(4)
		div = browser.find_by_id('Show0')
		while (hasattr(div,'html') == False):

			browser.find_by_id('btnSearch').click()
			time.sleep(5)
			div = browser.find_by_id('Show0')

		divh = div.html
		p = re.compile(r'[1-9]\d*\)</span>')
		ns = p.findall(divh)

		f1.write(date1s + "~" + date2s + ":")

		while (ns == "[]"):
			browser.find_by_id('btnSearch').click()
			time.sleep(4)
			div = browser.find_by_id('Show0')

			divh = div.html
			p = re.compile(r'[1-9]\d*\)</span>')
			ns = p.findall(divh)

		for nss in ns:
			nsss = nss[:-8]
			f1.write(nsss + " ")
			print nsss
		f1.write("\n")

	f1.close()




