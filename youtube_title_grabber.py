from bs4 import BeautifulSoup
from requests.exceptions import ConnectTimeout,ReadTimeout,ConnectionError
import os,re,requests,time,random,codecs,json,chardet,winsound,shutil

def read_file(filename):
	with codecs.open(filename, "r", encoding="utf-8") as file_reader:
		lines = file_reader.readlines()

	ill_chars = ['\r','\n']
	_ = []
	for line in lines:
		for ic in ill_chars:
			line = line.replace(ic,'')
		_.append(line)
	filtered_lines = _
	return filtered_lines

def write_file(filename, strs,mode="w"):
	import codecs
	with codecs.open(filename, mode, encoding='utf-8') as file_appender:
		file_appender.writelines(strs)

def get_html(url):
	"""Returns HTML beautiful soup 4 object"""
	while True:
		try:
			r = requests.get(url=url, timeout=10)
			break
		except ConnectTimeout:
			time.sleep(5)
			alert_tone()
			print("retrying to download page")			
		except ReadTimeout:
			time.sleep(5)
			alert_tone()
			print("retrying to download page")
		except ConnectionError:
			time.sleep(5)
			alert_tone()
			print("retrying to download page")

	r.encoding = r.apparent_encoding
	return BeautifulSoup( r.text, features="html.parser")

def get_site_title(url):
	page = get_html(url)
	YouTube_title = page.title.text.replace(" - YouTube","")
	return YouTube_title

lines = read_file('YouTube.txt')
title_urls = '\n'.join([get_site_title(url) + ' - ' + url for url in lines])
write_file('YouTube_.txt', title_urls,mode="w")
print(title_urls)