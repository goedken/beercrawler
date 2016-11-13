import scrapy
import string
from scrapy.loader import ItemLoader
from beercrawler.items import Beer

beerids = []
stopwords = ['brewery', 'brewing', 'co', 'company', 'restaurant', '&', 'brewpub', 'inc', 'spirits']


class UntappdSpider(scrapy.Spider):
    name = "untappd"
    allowed_domains = ["https://untappd.com/beer/"]
    start_urls = ['https://untappd.com/beer/']

    # print "about to crawl " + name
    # numToCrawl = raw_input("How many beers do you want to crawl? ")

    i = 1
    while i < 5000:  # SET HOW MANY PAGES YOU WANT TO CRAWL HERE
        start_urls.append('https://untappd.com/beer/' + str(i))
        i += 1

    def parse(self, response):
        f = open('untappdfiles/%s.html' % response.url.split('/')[5], 'w')
        f.write(response.body)
        # print "RESPONSE URL ----------------------" + response.url
        index = 0
        # print '---------------------------------------------------------------------'
        # print response.url
        # print response.request.url
        # print '---------------------------------------------------------------------'
        index += 1
        for beer in response.css('body'):

            abv1 = beer.css('div.details p.abv::text').extract_first().strip().split(' ')[0]
            abv = abv1.encode('ascii', 'ignore')
            abv = abv[:-1]

            beerid = int(response.url.split('/')[5])
            name = beer.css('div.name h1::text').extract_first().strip()
            breweryoriginal = beer.css('p.brewery a::text').extract_first().strip()

            brewerywords = breweryoriginal.split()
            brewerytrimmed = [word for word in brewerywords if word.lower() not in stopwords]
            brewery = ' '.join(brewerytrimmed)

            brewery = brewery.replace(".", "")
            brewery = brewery.replace(",", "")

            style = beer.css('p.style::text').extract_first().strip()
            rating = beer.css('p.rating span.num::text').extract_first().split(')')[0][1:]

            # print '---------------------------------------------------------------------'
            # print beerids
            # print '---------------------------------------------------------------------'

            if beerid not in beerids:
                beeritem = Beer()
                beeritem['id'] = beerid
                beeritem['name'] = name
                beeritem['brewery'] = brewery
                beeritem['breweryoriginal'] = breweryoriginal
                beeritem['abv'] = abv
                beeritem['style'] = style
                beeritem['rating'] = rating

                link = 'https://untappd.com' + beer.css('div.name p.brewery a::attr(href)').extract_first()

            # print '0000000000000000000000000000000000000000000000000'
            # print beeritem
            # print link
            #
                global beerids
                beerids.append(beerid)
                yield scrapy.Request(link, callback=self.parse_page2, meta={'item': beeritem}, dont_filter=True)
            # request.meta['beeritem'] = beeritem
            # yield request
            #yield beer
            #
            # yield {
            #     'id': int(response.url.split('/')[5]),
            #     'name': beer.css('div.name h1::text').extract_first().strip(),
            #     'brewery': beer.css('p.brewery a::text').extract_first().strip(),
            #     'abv': abv,
            #     # 'ibu': beer.css('div.details p.ibu::text').extract_first().strip().split(' ')[0],
            #     'style': beer.css('p.style::text').extract_first().strip(),
            #     'rating': beer.css('p.rating span.num::text').extract_first().split(')')[0][1:],
            #     #'state': beeritem['state'],
            #     #'country': beeritem['country'],
            # }

    def parse_page2(self, response):
        beeritem = response.meta['item']

        both = response.css('div.name p.brewery::text').extract_first().strip().split(',')[1].strip().replace("\t", "")
        # print '^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^'
        # for thing in both.spl:
        #     print thing.strip().replace("\t", "")
        # print both
        beeritem['state'] = both.split(' ', 1)[0].strip()
        beeritem['country'] = both.split(' ', 1)[1].strip()
        # print beeritem['state']
        # print beeritem['country']


        # print '----------------------------------------------------------'
        # print beeritem

        return beeritem
