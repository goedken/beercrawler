import scrapy
import json
import string
from beercrawler.items import Beer
import unicodedata
from scrapy.loader import ItemLoader
#from beercrawler.items import BeercrawlerItem

stopwords = ['brewery', 'brewing', 'co', 'company', 'restaurant', '&', 'brewpub', 'inc', 'spirits']

beerids = []


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
        if len(listToSearch) != 6000:  # SET HOW MANY PAGES YOU WANT TO CRAWL HERE
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
            abvIndex = abvraw.find('%', 40) - 5
            if abvraw[abvIndex:abvIndex+4].strip() == '/div':
                abvtext = '"'
            else:
                abvtext = abvraw[abvIndex:abvIndex+4].strip()
                # if int(abvtext) < 1:
                #     print '------------------------------------------------------------------'
            # print '000000000000000000000000000000000000000000000000000000000000000000000000'
            # print abvraw[abvIndex:abvIndex+4]
            # print abvIndex



            beerid = int(response.url.split('/')[6])
            name = beer.css('div.titleBar h1::text').extract_first()
            breweryoriginal = beer.css('div.titleBar h1 span::text').extract_first()[3:]

            brewerywords = breweryoriginal.split()
            brewerytrimmed = [word for word in brewerywords if word.lower() not in stopwords]
            brewery = ' '.join(brewerytrimmed)
            # brewery = brewery.encode('ascii', 'ignore')
            # translator = string.maketrans("", string.punctuation)

            brewery = brewery.replace(".", "")
            brewery = brewery.replace(",", "")

            state = beer.css('div.break a[href*=US]::text')[0].extract()
            country = beer.css('div.break a[href*=US]::text')[1].extract()
            style = beer.css('div.break a[href*=style] b::text').extract_first()
            rating = beer.css('span.ba-ravg::text').extract_first()
            abv = abvtext

            if beerid not in beerids:
                beeritem = Beer()
                beeritem['id'] = beerid
                beeritem['name'] = name
                beeritem['brewery'] = brewery
                beeritem['breweryoriginal'] = breweryoriginal
                beeritem['abv'] = abv
                beeritem['style'] = style
                beeritem['rating'] = rating
                beeritem['state'] = state
                beeritem['country'] = country

                global beerids
                beerids.append(beerid)

                yield beeritem



                # {
                #     'id': int(response.url.split('/')[6]),
                #     'name': beer.css('div.titleBar h1::text').extract_first(),
                #     'brewery': beer.css('div.titleBar h1 span::text').extract_first()[3:],
                #     'state': beer.css('div.break a[href*=US]::text')[0].extract(),
                #     'country': beer.css('div.break a[href*=US]::text')[1].extract(),
                #     'style': beer.css('div.break a[href*=style] b::text').extract_first(),
                #     'rating': beer.css('span.ba-ravg::text').extract_first(),
                #     'abv': abvtext
                #     # 'name': beer.css('ul li a[href*=profile]::attr(href)').extract()
                # }