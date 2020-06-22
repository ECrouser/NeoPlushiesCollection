

import requests
from bs4 import BeautifulSoup
import re
import copy

# import myotherfile
# myotherfile.myfunc()

# r
# rb
with open("JNplushielist.html",'r') as f:
	raw_JN_output_cached = f.read() # f.readlines() -> []
with open("collectionpage_intro_section.html",'r') as f:
	intro_section_html = f.read()
# with open("JNmywishlist.html",'r') as f:
# 	JN_wishlist_cached = f.read()

JN_wishlist_URL = 'https://items.jellyneo.net/mywishes/ethegreat1245/225909/?order_by=1&show_obtained'

def get_webpage_soup(path, get_new=False):
	if get_new:
		if not path.startswith('http'):
			raise Exception('Provide valid URL if getting new')
		page = requests.get(path)
		soup = BeautifulSoup(page.content, 'html.parser')
		open('JNmywishlist.html', 'wb').write(page.content)
	else:
		if not path.endswith('.html'):
			raise Exception('Provide valid file name if getting cached')
		with open(path, 'r') as f:
			cached_path = f.read()
		soup = BeautifulSoup(cached_path, 'html.parser')

	return soup


def sanitize_title(title):
	invalid_start_chars = ['0','1','2','3','4','5','6','7','8','9']
	if title[0] in invalid_start_chars:
		title = '_' + title
	san_title = re.sub('\W', '_', title)

	return san_title
	#pass


def obtained_dict_maker(page_path, refresh_from_web=False):
	soup = get_webpage_soup(page_path, get_new=refresh_from_web)

	total_dict = {}
	item_list = soup.find_all('img', class_='item-result-image')
	for counter, item in enumerate(item_list):
		a = item.parent
		obtained_status = a.has_attr('class')
		title = item.attrs['title']
		san_title = sanitize_title(title)
		item = re.sub(' ', '-', san_title)
		total_dict[counter] = (san_title, obtained_status)

	return total_dict


# def title_class_maker(page_path, include_unobtained=False):
# 	soup = get_webpage_soup(page_path)
	
# 	if include_unobtained:
# 		item_list = soup.find_all('img', class_='item-result-image')
# 		for item in item_list:
# 			title = item.attrs['title']
# 			san_title = sanitize_title(title)
# 			item = re.sub(' ', '-', san_title)
# 	else:
# 		item_list = soup.find_all('a', class_='wishlist-obtained')
# 		for item in item_list:
# 			title = item.find('img').attrs['title']
# 			san_title = sanitize_title(title)
# 			item = re.sub(' ', '-', san_title)
# 	return item_list


def process_html_items(html_raw, obtained_dict):
	soup = BeautifulSoup(html_raw, 'html.parser')
	item_box = soup.find('div', class_='wishlist-box')
	item_box.h1.string = 'Could a Non-Functioning Person Do All This??'
	item_table = soup.find('table', class_='wishlist-table')
	item_list = item_table.find_all('td')

	for counter, item in enumerate(item_list):
		dict_item = obtained_dict[counter]
		item['class'] = 'container'
		image = item.find('img')
#		image['class'] = dict_item[0]
		if dict_item[1] == False:
			image['class'] = 'gray'
			overlay_div = BeautifulSoup('<div><b>Still Needed</b></div>', 'html.parser')
			overlay_div.div['class'] = 'overlay'
			item.insert(1, overlay_div)
	
	return soup

def script_builder(intro_section, items_section):
	intro_soup = BeautifulSoup(intro_section, 'html.parser')
	soup = items_section

	soup.style.replace_with(intro_soup)
	open('index.html', 'w').write(soup.prettify())
	return soup



# Next more advanced step: use Selenium to request petpage code from https://items.jellyneo.net/wishlists/code/225909/

refresh = True

if refresh:
	path = JN_wishlist_URL
else:
	path = 'JNmywishlist.html'

mydict = obtained_dict_maker(page_path=path, refresh_from_web=refresh)
collection_items = process_html_items(raw_JN_output_cached, mydict)
script_builder(intro_section=intro_section_html, items_section=collection_items)