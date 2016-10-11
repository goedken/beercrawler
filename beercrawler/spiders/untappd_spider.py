import scrapy

class BeerSpider(scrapy.Spider):
    name = "untappd"
    allowed_domains = ["https://untappd.com/beer/"]
    start_urls = ['https://untappd.com/beer/']

    i = 1
    while i < 4000:
        start_urls.append('https://untappd.com/beer/' + str(i))
        i += 1

    def parse(self, response):
        f = open('untappdfiles/%s.html' % response.url.split('/')[5], 'w')
        f.write(response.body)
        print "RESPONSE URL ----------------------" + response.url
        for beer in response.css('body'):
            yield {
                'id': int(response.url.split('/')[5]),
                'name': beer.css('div.name h1::text').extract(),
                'brewery': beer.css('p.brewery a::text').extract(),
                'abv': beer.css('div.details p.abv::text').extract_first().strip().split(' ')[0],
                'ibu': beer.css('div.details p.ibu::text').extract_first().strip().split(' ')[0],
                'style': beer.css('p.style::text').extract(),
                'rating': beer.css('p.rating span.num::text').extract_first().split(')')[0][1:],
            }