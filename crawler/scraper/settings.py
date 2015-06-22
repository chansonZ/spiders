""" Wheels project settings. See: http://doc.scrapy.org/en/latest/topics/settings.html """


BOT_NAME = 'scraper'
SPIDER_MODULES = ['scraper.spiders']
NEWSPIDER_MODULE = 'scraper.spiders'

# The middleware uses Scrapy's hook system where the values from 0 to 1000 correspond to the sequence order.
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#std:setting-DOWNLOADER_MIDDLEWARES_BASE
# We have to disable the default user-agent before we activate a new one.

DOWNLOADER_MIDDLEWARES = {'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware': None,
                          'scraper.middlewares.user_agents.RotateUserAgentMiddleware': 400}

ITEM_PIPELINES = {'scraper.pipelines.DumpDuplicates': 300,
                  'scraper.pipelines.DumpProductsWithoutReview': 200,
                  'scraper.pipelines.SavePricesToFileTree': 400}
