import scrapy
import re


class CweSpiderSpider(scrapy.Spider):
    name = 'cwe_spider'

    def __init__(self, *args, **kwargs): 
        super(CweSpiderSpider, self).__init__(*args, **kwargs) 
        self.start_urls = [kwargs.get('url')]

    def parse(self, response):
        def join_clean(texts):
            return re.sub(r'\s+', ' ', ' '.join(texts)).strip()

        relations = {}
        for relation in response.xpath("//div[@id='Relationships']//div[@id='relevant_table']"):
            key = relation.xpath(".//div[@class='reltable']/text()").get()
            value = [response.request.url + i for i in relation.xpath(".//div[@class='tabledetail']//td/a/@href").getall()]
            relations[key] = value

        injection = []
        for relation in response.xpath("//div[@id='Modes_Of_Introduction']//div[@class='tabledetail']"):
            data = relation.xpath(".//td/text()").getall()
            injection.append(data)

        notes = {}
        for relation in response.xpath("//div[@id='Notes']"):
            key = relation.xpath(".//p[@class='subheading']/text()").get()
            value = " ".join(relation.xpath(".//div[@class='detail']//div[@class='indent']//div[@class='indent']/node()").getall())
            notes[key] = value

        related_attack_pattern = []
        for relation in response.xpath("//div[@id='Related_Attack_Patterns']//div[@class='tabledetail']"):
            data = relation.xpath(".//td/node()").getall()
            related_attack_pattern.append(data)


        yield {
            'desc_short': join_clean(response.xpath("//div[@id='Description']//div[@class='indent']/text()").getall()),
            'desc': join_clean(response.xpath("//div[@id='Extended_Description']//div[@class='indent']//p/text()").getall()),
            'relations': relations,
            'injection': injection,
            'notes': notes,
            'related_attack_pattern': related_attack_pattern,
            'created': response.xpath("((//div[@id='Content_History']//tbody)[1]//tr//td)[1]/text()").get(),
            'modified': response.xpath("((//div[@id='Content_History']//tbody)[2]//tr)[last() - 1]/td/text()").get(),
        }
