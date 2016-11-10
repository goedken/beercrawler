import scrapy
import json
import unicodedata
from scrapy.loader import ItemLoader
#from beercrawler.items import BeercrawlerItem


class BeerSpider(scrapy.Spider):
    name = "beers"

    with open('beerlinks.json') as urlList:
        data = json.load(urlList)

    list = []
    i = 0
    while i < len(data):
        j = 0
        while j < len(data[i]['name']):
            list.append(data[i]['name'][j])
            j += 1
        i += 1

    start_urls = [
        'https://www.beeradvocate.com/beer/profile/287/1093/'
    ]

    listToSearch = []
    #
    #
    # print "you are about to name
    # numToCrawl = raw_input("How many beers would you like to crawl (up to 40000)? ")

    for url in list:
        # print url
        if len(listToSearch) != 10: # SET HOW MANY PAGES YOU WANT TO CRAWL HERE
            listToSearch.append(url)
        else:
            break

    for url in listToSearch:
        stringToAdd = "https://www.beeradvocate.com" + url
        start_urls.append(stringToAdd)

    def parse(self, response):
        f = open('beerfiles/%s.html' % response.url.split('/')[6], 'w+')
        f.write(response.body)
        for beer in response.css('body'):
            abvraw = beer.css('div.break')[1].extract()
            abvraw.encode('ascii', 'ignore')
            abvIndex = abvraw.find('%', 40) - 4
            if abvraw[abvIndex:abvIndex+4] == '/div':
                abvtext = '"'
            else:
                abvtext = abvraw[abvIndex:abvIndex+4]
            # print '000000000000000000000000000000000000000000000000000000000000000000000000'
            # print abvraw[abvIndex:abvIndex+4]
            # print abvIndex
            yield {
                'id': int(response.url.split('/')[6]),
                'name': beer.css('div.titleBar h1::text').extract_first(),
                'brewery': beer.css('div.titleBar h1 span::text').extract_first()[3:],
                'state': beer.css('div.break a[href*=US]::text')[0].extract(),
                'country': beer.css('div.break a[href*=US]::text')[1].extract(),
                'style': beer.css('div.break a[href*=style] b::text').extract_first(),
                'rating': beer.css('span.ba-ravg::text').extract_first(),
                'abv': abvtext
                # 'name': beer.css('ul li a[href*=profile]::attr(href)').extract()
            }