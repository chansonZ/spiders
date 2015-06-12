""" This module provides a pool of user-agents for the spider. See:
        - http://tangww.com/2013/06/UsingRandomAgent/
        - http://www.whatsmyuseragent.com/CommonUserAgents
"""

from random import choice
from scrapy.contrib.downloadermiddleware.useragent import UserAgentMiddleware


USER_AGENTS = ['Mozilla/5.0; Windows NT 6.1; WOW64; Trident/7.0; rv:11.0; like Gecko',
               'Mozilla/5.0; Windows NT 6.2; WOW64; rv:27.0; Gecko/20100101 Firefox/27.0',
               'Mozilla/5.0; Windows NT 6.1; WOW64; AppleWebKit/537.36 ;KHTML, like Gecko; Chrome/36.0.1985.143 Safari/537.36',
               'Mozilla/5.0; iPhone; CPU iPhone OS 8_1_2 like Mac OS X; AppleWebKit/600.1.4 ;KHTML, like Gecko; Version/8.0 Mobile/12B440 Safari/600.1.4',
               'Mozilla/5.0; Macintosh; Intel Mac OS X 10_10_2; AppleWebKit/537.36 ;KHTML, like Gecko; Chrome/40.0.2214.111 Safari/537.36',
               'Mozilla/5.0; compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html;',
               'Mozilla/5.0; Windows NT 6.3; WOW64; Trident/7.0; rv:11.0; like Gecko',
               'Mozilla/5.0; compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/7.0;',
               'Mozilla/5.0; iPhone; CPU iPhone OS 8_1_3 like Mac OS X; AppleWebKit/600.1.4 ;KHTML, like Gecko; Version/8.0 Mobile/12B466 Safari/600.1.4',
               'Mozilla/5.0; iPhone; CPU iPhone OS 7_1_2 like Mac OS X; AppleWebKit/537.51.2 ;KHTML, like Gecko; Version/7.0 Mobile/11D257 Safari/9537.53',
               'Mozilla/5.0; Windows NT 6.1; rv:35.0; Gecko/20100101 Firefox/35.0',
               'Mozilla/5.0; Windows NT 6.1; WOW64; rv:35.0; Gecko/20100101 Firefox/35.0',
               'Mozilla/5.0; Windows NT 6.3; WOW64; AppleWebKit/537.36 ;KHTML, like Gecko; Chrome/39.0.2171.95 Safari/537.36',
               'Mozilla/5.0; Windows NT 6.1; rv:34.0; Gecko/20100101 Firefox/34.0',
               'Mozilla/5.0; Windows NT 6.1; WOW64; AppleWebKit/537.36 ;KHTML, like Gecko; Chrome/40.0.2214.115 Safari/537.36',
               'Mozilla/5.0; Windows NT 6.1; rv:36.0; Gecko/20100101 Firefox/36.0',
               'Mozilla/5.0; Windows NT 6.1; WOW64; rv:36.0; Gecko/20100101 Firefox/36.0',
               'Mozilla/5.0; Windows NT 6.1; WOW64; AppleWebKit/537.36 ;KHTML, like Gecko; Chrome/40.0.2214.111 Safari/537.36',
               'Mozilla/5.0; Windows NT 6.1; WOW64; rv:34.0; Gecko/20100101 Firefox/34.0',
               'Mozilla/5.0; Windows NT 6.3; WOW64; rv:35.0; Gecko/20100101 Firefox/35.0',
               'Mozilla/5.0; Windows NT 6.3; WOW64; rv:36.0; Gecko/20100101 Firefox/36.0',
               'Mozilla/5.0; iPhone; CPU iPhone OS 8_2 like Mac OS X; AppleWebKit/600.1.4 ;KHTML, like Gecko; Version/8.0 Mobile/12D508 Safari/600.1.4',
               'Mozilla/5.0; iPad; CPU OS 8_1_2 like Mac OS X; AppleWebKit/600.1.4 ;KHTML, like Gecko; Version/8.0 Mobile/12B440 Safari/600.1.4',
               'Mozilla/5.0; Windows NT 5.1; rv:36.0; Gecko/20100101 Firefox/36.0']


class RotateUserAgentMiddleware(UserAgentMiddleware):

    def process_request(self, request, spider):
        request.headers.setdefault('User-Agent', choice(USER_AGENTS))

