""" Fulcrum project settings. For other settings, see: http://doc.scrapy.org/en/latest/topics/settings.html """
# -*- coding: utf-8 -*-


BOT_NAME = 'scraper'
SPIDER_MODULES = ['scraper.spiders']
NEWSPIDER_MODULE = 'scraper.spiders'

# The middleware uses Scrapy's hook system where the the values are the middleware orders.
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#std:setting-DOWNLOADER_MIDDLEWARES_BASE
DOWNLOADER_MIDDLEWARES = {'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware': None,
                          'scraper.middlewares.user_agents.RotateUserAgentMiddleware': 400}