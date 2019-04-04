from bs4 import BeautifulSoup
from requests.exceptions import ConnectTimeout,ReadTimeout,ConnectionError
import os,re,requests,time,random,codecs,json,chardet,winsound,shutil,configparser

utube_title_seperating_flag = ' =u= '

config = configparser.ConfigParser()
config.readfp(codecs.open("config.ini", "r", "utf8"))

get_utube_title_choice = config['GETTING_UTUBE_VIDEO_TITLE']['GET_TITLE']
Get_utube_video_title_Input_File_Name = config['GETTING_UTUBE_VIDEO_TITLE']['Input_File_Name']
Get_utube_video_title_Output_File_Name = config['GETTING_UTUBE_VIDEO_TITLE']['Output_File_Name']
Get_utube_video_title_Show_Output = config['GETTING_UTUBE_VIDEO_TITLE']['Show_Output']

sort_choice = config['SORTING']['Sort']
sorting_tag_list = config['SORTING']['Tag_List'].split(',')
Sorting_Input_File_Name = config['SORTING']['Input_File_Name']
Sorting_Output_File_Name = config['SORTING']['Output_File_Name']
Sorting_Show_Output = config['SORTING']['Show_Output']


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



def list_utbube_title(filename):
	lines = read_file(filename)
	return [get_site_title(url) + utube_title_seperating_flag + url for url in lines]	

def find_tag_in_list(target_li,tag):
	return [stri for stri in target_li if tag in stri]


def sort_utube_urls_by_tag(filename,tag_list):
	titles = read_file(filename)
	sorted_li_1 = []
	sorted_li_2 = []
	sorted_li = []
	for tag in tag_list:
		for stri in titles:
			stri_ = stri.split(utube_title_seperating_flag)[0]
			if tag in stri_:
				sorted_li_1.append(stri)
			else:
				sorted_li_2.append(stri)
		sorted_li = sorted_li + sorted_li_1
		titles = sorted_li_2
		sorted_li_1 = []
		sorted_li_2 = []

	return sorted_li + titles


if(get_utube_title_choice == 'Yes'):
	title_urls = list_utbube_title(Get_utube_video_title_Input_File_Name)
	if(get_utube_title_choice == 'Yes'):
		print(title_urls)
	title_urls = '\n'.join(title_urls)
	write_file(Sorting_Output_File_Name, title_urls,mode="w")
	

if(sort_choice == 'Yes'):
	sorted_title_urls = sort_utube_urls_by_tag(Sorting_Input_File_Name,sorting_tag_list)
	if(Sorting_Show_Output == 'Yes'):
		print(sorted_title_urls)
	sorted_title_urls ='\n'.join(sorted_title_urls)
	write_file(Sorting_Output_File_Name, sorted_title_urls,mode="w")

