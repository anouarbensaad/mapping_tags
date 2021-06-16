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

def strect_gl():
    """
    Print list of all ads
    """
    instance = mapping_tags.Mappingtags(url=url,maps=[])
    content = instance.get_contents()
    opened_tags=instance.opened_tags(content)
    closed_tags=instance.closed_tags(content)
    print(instance.strecutre_general_maps(opened_tags,closed_tags))



if __name__ == "__main__":
    if(url):
        if(maptype == "global"):
            strect_gl()