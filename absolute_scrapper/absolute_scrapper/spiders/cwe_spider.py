import scrapy
import re


class CweSpiderSpider(scrapy.Spider):
    name = 'cwe_spider'

    def __init__(self, *args, **kwargs): 
        super(CweSpiderSpider, self).__init__(*args, **kwargs) 
        self.start_urls = [kwargs.get('url')]

    def parse(self, response):
        def join_clean(texts):
            result = re.sub(r'\s+', ' ', ' '.join(texts)).strip()
            return re.sub('href=\"/', 'href=\"https://cwe.mitre.org/', result)

        relations = {}
        for relation in response.xpath("//div[@id='Relationships']//div[@id='relevant_table']"):
            key = relation.xpath(".//div[@class='reltable']/text()").get()
            value = [join_clean(i.getall()) for i in relation.xpath(".//div[@class='tabledetail']//td//a")]
            relations[key] = value

        # NOTES
        headings = response.xpath("//div[@id='Notes']//p[@class='subheading']/text()").getall()
        content = [join_clean(i.xpath("./node()").getall()) for i in response.xpath("//div[@id='Notes']//div[@class='detail']//div[@class='indent']//div[@class='indent']")]
        notes = {
            "headings": headings, 
            "content": content,
        }


        yield {
            'title': response.xpath("//h2/text()").get(),
            'desc': join_clean(response.xpath("//div[@id='Description']//div[@class='indent']/node()").getall()),
            'content': join_clean(response.xpath("//div[@id='Extended_Description']//div[@class='indent']/node()").getall()),
            'relations': relations,
            'injection': [{"phase": i.xpath(".//td[position()=1]/text()").get(), "note": join_clean(i.xpath(".//td[position()=2]/node()").getall()),} for i in response.xpath("//div[@id='Modes_Of_Introduction']//div[@class='tabledetail']//tr[position()>1]")],
            'notes': notes,
            'related_attack_pattern': [{"link": i.xpath(".//td[position()=1]/a").get(), "name": i.xpath(".//td[position()=2]/text()").get(),} for i in response.xpath("//div[@id='Related_Attack_Patterns']//div[@class='tabledetail']//tr[position()>1] ")],
            'created': response.xpath("((//div[@id='Content_History']//tbody)[1]//tr//td)[1]/text()").get(),
            'modified': response.xpath("((//div[@id='Content_History']//tbody)[2]//tr)[last() - 1]/td/text()").get(),
        }
