import requests
from random import choice

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/74.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:61.0) Gecko/20100101 Firefox/74.0"
]

session_ua = choice(user_agents)
request_headers = {"User-Agent": session_ua}

class RequestException(Exception):
    pass

class Requester:
    
    def __init__(self,url,proxy):
        self.url = url
        self.cookies = proxy
    
    def get_content(self):
        """
        return text contents of html page from url.
        """
        response = requests.get(self.url,request_headers)
        if response.status_code == 301:
            raise RequestException("Not Authorized Content")
        if response.status_code == 404:
            raise RequestException("Not Found Content")
        return response.text