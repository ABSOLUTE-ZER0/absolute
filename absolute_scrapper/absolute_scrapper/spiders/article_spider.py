import scrapy
import re

class ArticleSpiderSpider(scrapy.Spider):
    name = 'article_spider'

    def __init__(self, *args, **kwargs): 
        super(ArticleSpiderSpider, self).__init__(*args, **kwargs) 
        self.start_urls = [kwargs.get('url')] 

    def parse(self, response):
        def join_clean(texts):
            return re.sub(r'\s+', ' ', ' '.join(texts)).strip()
    
        ct = response.headers.get("content-type", "").lower()
        if(ct != 'text/html'):
            yield {
                'data': "Cannot scrape non html documents"
            }
            return 0

        yield {
            'data': join_clean(response.xpath("//body//div/text()|//body//p/text()").getall()),
        }

# EXAMPLE: scrapy crawl article_spider -a url="http://cwe.mitre.org/data/definitions/611.html"
