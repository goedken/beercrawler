There are three crawlers in beercrawler. 

1. 'beerlinks' crawls for the BeerAdvocate URLs to be crawled by 'beers'. Since BeerAdvocate has no master list of beers to crawl through,
we start by searching for 'ale' in the BeerAdvocate search bar and then loop through the beers 25 search results per page at a time. 
This crawler results in a json file with a giant list of URLs to BeerAdvocate beers. Run this crawler by typing <code>scrapy crawl beerlinks -o beerlinks.json</code>

2. 'beers' crawls the BeerAdvocate URLs in beerlinks.json. It first opens the json file, then crawls through each link. Outputs a .csv file
called beers.csv that contains data about the beers, specifically its ID (generated from its URL), brewery, name, style, abv, rating, state,
and country. It also stores each HTML file that it crawled through in a subfolder called 'beerfiles'. This folder must be created before
calling the crawler in order for the HTML files to be saved.

3. 'untappd' crawls Untappd beers by inputting integers into the end of the url 'http://untappd.com/beer/'. Does this however many times you
want. Currently gets the beer's ID (generated from the int provided at the end of the URL), brewery, name, style, abv, and rating. It also
stores each HTML file that it crawls to a subfolder called 'untappdfiles'. This folder must be created before calling the crawler in order
for the HTML files to be saved. 
