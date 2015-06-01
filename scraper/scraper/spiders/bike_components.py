from scrapy import Spider


class BikeComponents(Spider):
    name = 'bike_components'
    allowed_domains = ['bike-components.de']
    start_urls = ['https://www.bike-components.de/advanced_search_result.php?keywords=fulcrum']

    deals_list_xpath = '//li[@dealid]'
    item_fields = {
        'title': './/span[@itemscope]/meta[@itemprop="name"]/@content',
        'link': './/a/@href',
        'location': './/a/div[@class="deal-details"]/p[@class="location"]/text()',
        'original_price': './/a/div[@class="deal-prices"]/div[@class="deal-strikethrough-price"]/div[@class="strikethrough-wrapper"]/text()',
        'price': './/a/div[@class="deal-prices"]/div[@class="deal-price"]/text()',
        'end_date': './/span[@itemscope]/meta[@itemprop="availabilityEnds"]/@content'

    def parse(self, response):
        filename = response.url.split('/')[-2]
        with open(filename, 'wb') as f:
            f.write(response.body)