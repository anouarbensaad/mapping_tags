import sys
import re
import json

if sys.version_info < (3, 0):
    raise Exception("This program requires Python 3.0 or greater")

tags = []
strecture = {
	"mapping": []
}

class MappingException(Exception):
    pass

class MappingHtml:

    def __init__(self,content):
        self.content = content


    def opened_tags(self):
        """
        method to get all matches opened tags found.
        """
        if not self.content:
            raise MappingException("No content found to parse opened tags")
        regex=r'<(\w+)[^>]*>'
        matches=re.findall(re.compile(regex),self.content)
        return matches
    

    def tag_property(self,tag):
        """
        get a specific tag from getted contents.
        """
        if not self.content:
            raise MappingException("No content found to parse opened tags")
        
        if not tag:
            raise MappingException("No spécific tags found to parse")
        regex=rf'<{tag}(.+)[^>]*\>'
        matches=re.findall(re.compile(regex),self.content)
        if(not matches):
            raise MappingException("No Matches for this {0}".format(tag))
        return matches


    def closed_tags(self):
        """
        method to get all matches of opened tags found.
        """
        if not self.content:
            raise MappingException("No content found to parse closed tags")

        regex=r'</(\w+)>'
        matches=re.findall(re.compile(regex),self.content)
        return matches


    def tag_mapping(self,tag):
        """
        return the tag strecture.
        """
        if not self.content:
            raise MappingException("No content found to parse tags mapping")
        
        if not tag:
            raise MappingException("No spécific tag found to parse")
        regex=rf"(<{tag}>.+</{tag})"
        matches=re.findall(regex,self.content,flags=re.DOTALL)
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


    def parse_links(self):
        regexp = r'href=\"(.+)[^"]*("\s+)?(^>)?'
        matches=re.findall(regexp,self.content)
        return matches