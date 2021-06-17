import argparse
import sys
import mapping_tags

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

    parser.add_argument('-t', '--type', help='list mapping', dest='maptype',choices=['global', 'diff', 'links'])
    
    return parser.parse_args()


args = parse_args()
url = args.url
maptype = args.maptype

def strect_gl(content):
    """
    return tags strecture
    """
    opened_tags=instance.opened_tags(content)
    closed_tags=instance.closed_tags(content)
    return instance.strecutre_general_maps(opened_tags,closed_tags)

def close_open_diff(content):
    """
    return differences between closed and open tags
    """
    opened_tags=instance.opened_tags(content)
    closed_tags=instance.closed_tags(content)
    return instance.diff_tags(opened_tags,closed_tags)

def grab_links(content):
    """
    return all links from web
    """
    return instance.parse_links(content)

if __name__ == "__main__":
    if(url):
        instance = mapping_tags.Mappingtags(url=url)
        content = instance.get_contents()
        if(maptype == "global"):
            strect_gl(content)
        if(maptype == "diff"):
            close_open_diff(content)
        if(maptype == "links"):
            grab_links(content)