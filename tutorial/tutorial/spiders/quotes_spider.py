from pathlib import Path
import scrapy

### First Spider: initial requests, follow links, 
#   parse content to extract data

# class QuotesSpider(scrapy.Spider):
#     name = "quotes"

#     def start_requests(self):
#         urls = [
#             "https://quotes.toscrape.com/page/1/",
#             "https://quotes.toscrape.com/page/2/",
#         ]
#         for url in urls:
#             yield scrapy.Request(url=url, callback=self.parse)

#     def parse(self, response):
#         page = response.url.split("/")[-2]
#         filename = f"quotes-{page}.html"
#         Path(filename).write_bytes(response.body)
#         self.log(f"Saved file {filename}")

#################

### Shortcut to the start_requests method: provide a list 
#   to go to link automatically  
#   gets the data from each URL, processes it, and saves it as a file.

# class QuotesSpider(scrapy.Spider):
#     name = "quotes"
#     start_urls = [
#         "https://quotes.toscrape.com/page/1/",
#         "https://quotes.toscrape.com/page/2/",
#     ]

#     def parse(self, response):
#         page = response.url.split("/")[-2]
#         filename = f"quotes-{page}.html"
#         Path(filename).write_bytes(response.body)

####################

### Yield: generates many dictionaries containing the data extracted from the page

# class QuotesSpider(scrapy.Spider):
#     name = "quotes"
#     start_urls = [
#         "https://quotes.toscrape.com/page/1/",
#         "https://quotes.toscrape.com/page/2/",
#     ]

#     def parse(self, response):
#         for quote in response.css("div.quote"):
#             yield {
#                 "text": quote.css("span.text::text").get(),
#                 "author": quote.css("small.author::text").get(),
#                 "tags": quote.css("div.tags a.tag::text").getall(),
#             }

####################

### Follow links to next page

# class QuotesSpider(scrapy.Spider):
#     name = "quotes"
#     start_urls = [
#         "https://quotes.toscrape.com/page/1/",
#     ]

#     def parse(self, response):
#         for quote in response.css("div.quote"):
#             yield {
#                 "text": quote.css("span.text::text").get(),
#                 "author": quote.css("small.author::text").get(),
#                 "tags": quote.css("div.tags a.tag::text").getall(),
#             }

#         next_page = response.css("li.next a::attr(href)").get()
#         if next_page is not None:
#             next_page = response.urljoin(next_page)
#             yield scrapy.Request(next_page, callback=self.parse)

####################

### shortcut for creating Request objects

# class QuotesSpider(scrapy.Spider):
#     name = "quotes"
#     start_urls = [
#         "https://quotes.toscrape.com/page/1/",
#     ]

#     def parse(self, response):
#         # Extracting the quotes, authors, and tags
#         for quote in response.css("div.quote"):
#             yield {
#                 "text": quote.css("span.text::text").get(),
#                 "author": quote.css("span small::text").get(),
#                 "tags": quote.css("div.tags a.tag::text").getall(),
#             }

#         # Following pagination links
#         yield from response.follow_all(css="li.next a", callback=self.parse)

# "response.follow" supports relative URLs directly 
# - no need to call urljoin. Note that "response.follow" 
#  just returns a Request instance; you still have to yield this Request.


#############

# Scraping author info

# class AuthorSpider(scrapy.Spider):
#     name = "author"

#     start_urls = ["https://quotes.toscrape.com/"]

#     def parse(self, response):
#         author_page_links = response.css(".author + a")
#         yield from response.follow_all(author_page_links, self.parse_author)

#         pagination_links = response.css("li.next a")
#         yield from response.follow_all(pagination_links, self.parse)

#     def parse_author(self, response):
#         def extract_with_css(query):
#             return response.css(query).get(default="").strip()

#         yield {
#             "name": extract_with_css("h3.author-title::text"),
#             "birthdate": extract_with_css(".author-born-date::text"),
#             "bio": extract_with_css(".author-description::text"),
#         }


#############

# Spider Arguments

class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        url = "https://quotes.toscrape.com/"
        tag = getattr(self, "tag", None)
        if tag is not None:
            url = url + "tag/" + tag
        yield scrapy.Request(url, self.parse)

    def parse(self, response):
        for quote in response.css("div.quote"):
            yield {
                "text": quote.css("span.text::text").get(),
                "author": quote.css("small.author::text").get(),
            }

        next_page = response.css("li.next a::attr(href)").get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)