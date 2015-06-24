""" Wheels project settings. See: http://doc.scrapy.org/en/latest/topics/settings.html """


BOT_NAME = 'scraper'
SPIDER_MODULES = ['scraper.spiders']
NEWSPIDER_MODULE = 'scraper.spiders'

# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#std:setting-DOWNLOADER_MIDDLEWARES_BASE
DOWNLOADER_MIDDLEWARES = {'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware': None,
                          'scraper.middlewares.user_agents.RotateUserAgentMiddleware': 400}

ITEM_PIPELINES = {'scraper.pipelines.DumpDuplicates': 300,
                  'scraper.pipelines.CheckMissingFields': 200,
                  'scraper.pipelines.SavePricesToFileTree': 400}
