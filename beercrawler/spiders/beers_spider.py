import scrapy


class BeerSpider(scrapy.Spider):
    name = "beers"
    start_urls = [
        'https://www.beeradvocate.com/beer/profile/28743/136936/'
    ]

    def parse(self, response):
        for beer in response.css('body'):
            yield {
                'name': beer.css('div.titleBar h1::text').extract_first(),
                'brewery': beer.css('div.titleBar h1 span::text').extract_first()[3:],
                'state': beer.css('div.break a[href*=US]::text')[0].extract(),
                'country': beer.css('div.break a[href*=US]::text')[1].extract(),
                'style': beer.css('div.break a[href*=style] b::text').extract_first(),
                'abv': beer.xpath("//div[contains(@style, 'width:70%')]/text").extract()
            }

