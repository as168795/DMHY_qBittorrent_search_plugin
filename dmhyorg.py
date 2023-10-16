# VERSION: 2.02
# AUTHORS: hatn

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

try:
	import re
except ModuleNotFoundError:
	SystemExit
# import qBT modules
try:
	from novaprinter import prettyPrinter
	from helpers import retrieve_url
except ModuleNotFoundError:
	pass

class dmhyorg(object):
	url = "https://share.dmhy.org"
	name = "DMHY2"
	
	page_max = 6 # total: 80 * page_max
	supported_categories = {"all": 0, "anime": 2, "pictures": 3, "music": 4, "tv": 6, "games": 9}
	
	table_reg = r'<table[^>]*id="topic_list"[^>]*>\s*<thead>[\s\S]+?</thead>\s*<tbody>([\s\S]+?)</tbody>\s*</table>'
	tr_reg = r'(<tr[^>]*>[\s\S]+?</tr>)'
	reg = r'<tr\s+class="[^"]*">\s+<td\s+width="[^"]+">[\s\S]+?</td>\s+<td\s+width="[^"]+"\s+align="center">[\s\S]+?</td>\s+<td\s+class="title">[\s\S]*?<a\s+href="([^"]+)"\s+target="_blank"\s*>\s*([\s\S]+?)\s*?</a>[\s\S]+?</td>[\s\S]+?<td\s+nowrap="nowrap"\s+align="center">\s+<a\s+class="download-arrow arrow-magnet"\s+title="磁力下載"\s+href="([^"]+)">[^<]+</a>[\s\S]+?</td>\s+<td\s+nowrap="nowrap"\s+align="center">([\s\S]+?)</td>[^<]+<td\s+nowrap="nowrap"\s+align="center"><span class="btl_1">([\s\S]+?)</span></td>[^<]+<td\s+nowrap="nowrap"\s+align="center"><span\s+class="bts_1">([\s\S]+?)</span></td>[^<]+<td\s+nowrap="nowrap"\s+align="center">([\s\S]+?)</td>\s+<td\s+align="center"><a\s+href="[^"]+">[\s\S]+?</a></td>\s+</tr>'

	def get_data(self, url):
		html = retrieve_url(url)
		result = re.findall(self.table_reg, html)
		if len(result) == 0 :
			if __name__ == "__main__":
				print('test----', url, result) # test
			raise SystemExit
		html_raw = result[0]
		tr_raw = re.findall(self.tr_reg, html_raw)
		data, item, name = [], {}, ''
		for tr in tr_raw:
			result = re.findall(self.reg, tr)
			for v in result:
				name = re.compile(r'<[^>]+>', re.S).sub('', v[1]).replace('\t', '').replace('\n', '').replace('\xa0', '')
				item = {'link': v[2], 'name': name, 'desc_link': self.url + v[0], 'size': v[3], 'seeds': v[4], 'leech': v[5], 'engine_url': self.url}
				data.append(item)
				# data.append(name)
		# print(tr, data, len(data))
		# exit()
		return [data, len(data)]

	def search(self, what, cat = "all", maxpage = 99):
		page, cate, total = 1, self.supported_categories.get(cat, "0"), 0
		while True:
			url = "{}/topics/list/page/{}?keyword={}&sort_id={}&team_id=0&order=date-desc".format(self.url, page, what, cate)
			[data, len] = self.get_data(url)
			total += len
			for item in data:
				prettyPrinter(item)
			if page >= maxpage or page >= self.page_max or len < 80:
				break
			page += 1
		return total


""" test """
def main():
	args = sys.argv
	# python dmhy-org.py "异世界" 1 # 需urlencode编码参数 如果是对象则 urllib.parse.urlencode(params) -> name=John+Doe&age=30&city=New+York
	title = urllib.parse.quote(args[1]) if len(args[1]) > 0 else "game"
	maxpage = int(args[2]) if len(args[2]) > 0 else 99 # 最大页数
	dmhy = dmhyorg()
	total = dmhy.search(title, 'all', maxpage)
	print(total)

if __name__ == "__main__":
	import sys
	import urllib.parse
	main()
