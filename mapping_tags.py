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

class MappingException(Exception):
    pass

class Mappingtags:

    def __init__(self,url):
        self.url = url

    def get_contents(self):
        """
        return text contents of html page from url.
        """
        results = requests.get(self.url,headers=request_headers)
        return results.text

    def opened_tags(self,data):
        """
        method to get all matches opened tags found.
        """
        if not data:
            raise MappingException("No content found to parse opened tags")
        regex=r'<(\w+)[^>]*>'
        matches=re.findall(re.compile(regex),data)
        return matches
    
    def tag_property(self,data,tag):
        """
        get a specific tag from getted contents.
        """
        if not data:
            raise MappingException("No content found to parse opened tags")
        
        if not tag:
            raise MappingException("No spécific tags found to parse")
        regex=rf'<{tag}(.+)[^>]*\>'
        matches=re.findall(re.compile(regex),data)
        if(not matches):
            raise MappingException("No Matches for this {0}".format(tag))
        return matches

    def closed_tags(self,data):
        """
        method to get all matches of opened tags found.
        """
        if not data:
            raise MappingException("No content found to parse closed tags")

        regex=r'</(\w+)>'
        matches=re.findall(re.compile(regex),data)
        return matches

    def tag_mapping(self,data,tag):
        """
        return the tag strecture.
        """
        if not data:
            raise MappingException("No content found to parse tags mapping")
        
        if not tag:
            raise MappingException("No spécific tag found to parse")
        regex=rf"(<{tag}>.+</{tag})"
        matches=re.findall(regex,data,flags=re.DOTALL)
        return matches

    def parse_tag_mapping(self,properties):
        """
        return all matches of proprietes.
        parse a tag proprietes. 
        """
        regex=r'(\S+)=["\']?((?:.(?!["\']?\s+(?:\S+)=|\s*\/?[>"\']))+.)["\']?'
        matches=re.findall(regex,properties)
        return matches

    def strecutre_general_maps(self,opened_matches,closed_matches):
        """
        Return json object of open/closed tags duplicated..
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

    def diff_tags(self,opened,closed):
        """
        opened : all opeened tags
        closed : all closed tags
        return diffs between opened and closed tags.
        """
        return json.dumps({"mappings":{"diff":[x for x in opened if x not in closed]}})

    def parse_links(self,content):
        regexp = r'href=\"(.+)[^"]*("\s+)?(^>)?'
        matches=re.findall(regexp,content)
        return matches
