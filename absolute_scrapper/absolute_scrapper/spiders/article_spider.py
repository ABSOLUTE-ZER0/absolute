# THE FOLLOWING SPIDER IS NOT BEING USED AS OF NOW
# IT WORKS FINE BUT SCHEDULING SCRAPPER USING SCRAPYD TAKES FEW SECONDS TO START
# EVEN THOUGH BS4 IS SLOW, IT AVOIDS REMOTE REQUETS FOR DAEMON AND 
# BS4 EVEN AVOIDS FILE CREATION FOR STORING THE SCRAPPED DATA, READING IT AND THEN DELETING IT

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