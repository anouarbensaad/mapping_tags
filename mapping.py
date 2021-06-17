import argparse
import sys
import json
from modules.mappinghtml import MappingHtml
from modules.requester import Requester

if sys.version_info < (3, 0):
    raise Exception("This program requires Python 3.0 or greater")


def parser_error(errmsg):
    print("Usage: python " + sys.argv[0] + " [Options] use -h for help")
    sys.exit()


def parse_args():
    parser = argparse.ArgumentParser(epilog='\tExample: \r\npython ' + sys.argv[0] + " -u google.com")
    parser.error = parser_error
    parser._optionals.title = "\nOPTIONS"
    
    parser.add_argument('-u', '--url', help='xxxx',dest='url')
    parser.add_argument('-x', '--maptype', help='xxxx',dest='maptype', choices=['html', 'xml'])
    parser.add_argument('-m', '--mapping', help='list mapping', dest='mapstruct',choices=['global', 'diff', 'links'])
    parser.add_argument('-p', '--prop', help="properties_tags", dest="prop")  

    return parser.parse_args()


args = parse_args()
url = args.url
maptype = args.maptype
propriete = args.prop
mapstruct = args.mapstruct

def strect_gl():
    """
    return tags strecture
    """
    opened_tags=htmap.opened_tags()
    closed_tags=htmap.closed_tags()
    sys.stdout.write(htmap.strecutre_general_maps(opened_tags,closed_tags))


def close_open_diff():
    """
    return differences between closed and open tags
    """
    opened_tags=htmap.opened_tags()
    closed_tags=htmap.closed_tags()
    sys.stdout.write(htmap.diff_tags(opened_tags,closed_tags))


def grab_links():
    """
    return all links from web
    """
    return htmap.parse_links()


def tags_properties(prop):
    props = []
    for i in htmap.tag_property(prop):
        temp = [x.split("=") for x in i.strip().split(" ")]
        for x in temp:
            obj={}
            if (len(x)>1):
                obj[x[0]] = x[1].strip('"')
                props.append(obj)
    sys.stdout.write(json.dumps({prop:[props]}))


if __name__ == "__main__":
    if(url):
        req_ins = Requester(url=url,proxy=None)
        content = req_ins.get_content()
        if (maptype == "html"):
            htmap = MappingHtml(content=content)
            if(mapstruct == "global"):
                strect_gl()
            if(mapstruct == "diff"):
                close_open_diff()
            if(mapstruct == "links"):
                print(grab_links())
            if(propriete):
                tags_properties(propriete)