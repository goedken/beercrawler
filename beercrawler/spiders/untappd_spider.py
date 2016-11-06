import scrapy
from scrapy.loader import ItemLoader
from beercrawler.items import Beer


class BeerSpider(scrapy.Spider):
    name = "untappd"
    allowed_domains = ["https://untappd.com/beer/"]
    start_urls = ['https://untappd.com/beer/']

    numToCrawl = raw_input("How many untappd beers do you want to crawl? ")
    i = 1
    while i < int(numToCrawl):
        start_urls.append('https://untappd.com/beer/' + str(i))
        i += 1

    def parse(self, response):
        f = open('untappdfiles/%s.html' % response.url.split('/')[5], 'w')
        f.write(response.body)
        #print "RESPONSE URL ----------------------" + response.url
        for beer in response.css('body'):
            abv1 = beer.css('div.details p.abv::text').extract_first().strip().split(' ')[0]
            abv = abv1.encode('ascii', 'ignore')
            abv = abv[:-1]

            # beerid = int(response.url.split('/')[5])
            # name = beer.css('div.name h1::text').extract_first().strip()
            # brewery = beer.css('p.brewery a::text').extract_first().strip()
            # style = beer.css('p.style::text').extract_first().strip()
            # rating = beer.css('p.rating span.num::text').extract_first().split(')')[0][1:]
            #
            # beeritem = Beer()
            # beeritem['id'] = beerid
            # beeritem['name'] = name
            # beeritem['brewery'] = brewery
            # beeritem['abv'] = abv
            # beeritem['style'] = style
            # beeritem['rating'] = rating
            #
            # link = 'https://' + beer.css('div.name p.brewery a::attr(href)').extract_first()
            #
            # print '0000000000000000000000000000000000000000000000000'
            # print beeritem
            #
            # request = scrapy.Request(link, callback=self.parse_page2)
            # request.meta['beeritem'] = beeritem
            # yield request
            #yield beer
            #
            yield {
                'id': int(response.url.split('/')[5]),
                'name': beer.css('div.name h1::text').extract_first().strip(),
                'brewery': beer.css('p.brewery a::text').extract_first().strip(),
                'abv': abv,
                # 'ibu': beer.css('div.details p.ibu::text').extract_first().strip().split(' ')[0],
                'style': beer.css('p.style::text').extract_first().strip(),
                'rating': beer.css('p.rating span.num::text').extract_first().split(')')[0][1:],
                #'state': beeritem['state'],
                #'country': beeritem['country'],
            }

    def parse_page2(self, response):
        beeritem = response.meta['beeritem']

        both = response.css('div.name p.brewery::text').extract_first().strip().split(',')[1]
        print '^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^'
        print both
        beeritem['state'] = both.split(' ')[0]
        beeritem['country'] = both.split(' ')[1]

        # print '0000000000000000000000000000000000000000000000000000000000000000000000000'
        # print state
        # print country

        print '----------------------------------------------------------'
        print beeritem

        yield beeritem
