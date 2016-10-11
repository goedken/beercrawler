import scrapy


class BeerLinkSpider(scrapy.Spider):
    name = "beerlinks"

    start_urls = [
        'https://www.beeradvocate.com/search/?start=0&q=ale&qt=beer'
    ]

    i = 25
    while i < 40000:
        urlToAdd = 'https://www.beeradvocate.com/search/?start=' + str(i) + '&q=ale&qt=beer'
        start_urls.append(urlToAdd)
        i += 25

    def parse(self, response):
        for beerlink in response.css('body'):
            yield {
                'name': beerlink.css('ul li a[href*=profile]::attr(href)')[::2].extract()
            }
