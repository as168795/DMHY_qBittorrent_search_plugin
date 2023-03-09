
# VERSION: 2.00
# AUTHORS: xyau (xyauhideto@gmail.com)

# MIT License
#
# Copyright (c) 2018 xyau
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the right
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software i
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


# import qBT modules
try:
	import re
	from novaprinter import prettyPrinter
	from helpers import retrieve_url
except ModuleNotFoundError:
    pass

class dmhyorg(object):
	url = "https://share.dmhy.org"
	name = "DMHY"
	supported_categories = {"all": 0, "anime": 2, "pictures": 3, "music": 4, "tv": 6, "games": 9}
	
	table_reg = r'<table[^>]*id="topic_list"[^>]*>\s*<thead>[\s\S]+?</thead>\s*<tbody>([\s\S]+?)</tbody>\s*</table>'
	#table_reg = r'<table([^>]*)id="topic_list"([^>]*)>' #
	tr_reg = r'(<tr[^>]*>[\s\S]+?</tr>)'
	reg = r'<tr\s+class="[^"]*">\s+<td\s+width="[^"]+">[\s\S]+?</td>\s+<td\s+width="[^"]+"\s+align="center">[\s\S]+?</td>\s+<td\s+class="title">[\s\S]*?<a\s+href="([^"]+)"\s+target="_blank"\s*>\s*([\s\S]+?)\s*?</a>[\s\S]+?</td>[\s\S]+?<td\s+nowrap="nowrap"\s+align="center">\s+<a\s+class="download-arrow arrow-magnet"\s+title="磁力下載"\s+href="([^"]+)">[^<]+</a>[\s\S]+?</td>\s+<td\s+nowrap="nowrap"\s+align="center">([\s\S]+?)</td>[^<]+<td\s+nowrap="nowrap"\s+align="center"><span class="btl_1">([\s\S]+?)</span></td>[^<]+<td\s+nowrap="nowrap"\s+align="center"><span\s+class="bts_1">([\s\S]+?)</span></td>[^<]+<td\s+nowrap="nowrap"\s+align="center">([\s\S]+?)</td>\s+<td\s+align="center"><a\s+href="[^"]+">[\s\S]+?</a></td>\s+</tr>'

	def get_data(self, url):
		html = retrieve_url(url)
		result = re.findall(self.table_reg, html)
		"""if not result:
		print(result)
		exit()
		"""
		html_raw = result[0]
		tr_raw = re.findall(self.tr_reg, html_raw)
		#print(tr_raw[0])
		#exit()
		data, item, name = [], {}, ''
		for tr in tr_raw:
			result = re.findall(self.reg, tr)
			#print(result)
			#exit()
			for v in result:
				name = re.compile(r'<[^>]+>', re.S).sub('', v[1]).replace('\t', '').replace('\n', '').replace('\xa0', '')
				item = {'link': v[2], 'name': name, 'desc_link': self.url + v[0], 'size': v[3], 'seeds': v[4], 'leech': v[5], 'engine_url': self.url}
				data.append(item)
				#data.append(name)
		#print(tr, data, len(data))
		#exit()
		return [data, len(data)]

	def search(self, what, cat="all"):
		page, cate, total = 1, self.supported_categories.get(cat, "0"), 0
		while True:
			url = "{}/topics/list/page/{}?keyword={}&sort_id={}&team_id=0&order=date-desc".format(
			    self.url, page, what, cate)
			[data, len] = self.get_data(url)
			total += len
			for item in data:
				prettyPrinter(item)
			if page >= 2 or len < 80:
				break
			page += 1
		#return total

""" test
dmhy = dmhyorg()
total = dmhy.search('game', 'all')
print(total)
"""
