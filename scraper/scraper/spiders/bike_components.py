from scrapy import Spider


class BikeComponents(Spider):
    name = 'bike-components.de'

    allowed_domains = ['bike-components.de']
    start_urls = ['https://www.bike-components.de/advanced_search_result.php?keywords=fulcrum']

    def parse(self, response):
        filename = response.url.split('/')[-2]
        with open(filename, 'wb') as f:
            f.write(response.body)