import scrapy


class BeerSpider(scrapy.Spider):
    name = "untappd"

    start_urls = [
        'http://untappd.com/beer/1'
    ]

    i = 2
    while i < 3500:
        urlToAdd = 'http://untappd.com/beer/' + str(i)
        i += 1

    def parse(self, response):
        for beer in response.css('body'):
            yield {

            }
