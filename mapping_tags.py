import sys
from random import choice
import requests
import re
import json


user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/74.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:61.0) Gecko/20100101 Firefox/74.0"
]

session_ua = choice(user_agents)
request_headers = {"User-Agent": session_ua}

if sys.version_info < (3, 0):
    raise Exception("This program requires Python 3.0 or greater")

tags = []
strecture = {
	"mapping": []
}

class Mappingtags:
	def __init__(self,url,maps):
		self.url = url
		self.maps = maps

	def get_contents(self):
		results = requests.get(self.url,headers=request_headers)
		return results.text
	
	def opened_tags(self,data):
		regex=r'<(\w+)[^>]*>'
		matches=re.findall(re.compile(regex),data)
		return matches

	def closed_tags(self,data):
		regex=r'</(\w+)>'
		matches=re.findall(re.compile(regex),data)
		return matches

	def tag_mapping(self,data,tag):
		regex=rf"(<{tag}>.+</{tag})"
		matches=re.findall(regex,data,flags=re.DOTALL)
		return matches

	def parse_tag_mapping(self,array):
		regex=r'(\S+)=["\']?((?:.(?!["\']?\s+(?:\S+)=|\s*\/?[>"\']))+.)["\']?'
		for maps in array:
			print(maps)
			matches=re.findall(regex,maps)
			print(matches)

	def strecutre_general_maps(self,opened_matches,closed_matches):
		"""
		Return json object of open/closed tags duplicated.
		"""
		openedmappings = {}
		closedmappings = {}
		tmp = []
		tmp2= []
		for m in closed_matches:
			if m not in tmp2:
				tmp2.append(m)
				closedmappings[m] = closed_matches.count(m)
		for m in opened_matches:
			if m not in tmp:
				tmp.append(m)
				openedmappings[m] = opened_matches.count(m)
		return json.dumps({"mappings":{"opened_tag":[openedmappings]},"closed_tag":[closedmappings]})


instance = Mappingtags(url="http://127.0.0.1",maps={})

content = instance.get_contents()
opened_tags=instance.opened_tags(content)
closed_tags=instance.closed_tags(content)
print(instance.strecutre_general_maps(opened_tags,closed_tags))