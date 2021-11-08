import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
# from scrapy_splash import SplashRequest


class NvdCrawlerSpider(CrawlSpider):
    name = 'nvd_crawler'
    allowed_domains = ['nvd.nist.gov']
    url = 'https://nvd.nist.gov/vuln/search/results?isCpeNameSearch=false&results_type=overview&form_type=Basic&search_type=all&startIndex=0'

    def start_requests(self):
        yield scrapy.Request(url=self.url)

    # script = '''
    #     function main(splash, args)
    #         url = args.url
    #         splash:go(url)
    #         return splash:html()
    #     end
    # '''

    rules = (Rule(LinkExtractor(deny=('/vuln-metrics/cvss/'), restrict_xpaths='//table[@data-testid="vuln-results-table"]//a'), callback='parse_item', follow=True),
             Rule(LinkExtractor(restrict_xpaths='(//a[@data-testid="pagination-link-page->"])[2]')),)

    def parse_item(self, response):
        yield {
            'title': response.xpath('//h2//span[@data-testid="page-header-vuln-id"]/text()').get(),
            'warning': response.xpath('//p[@data-testid="vuln-warning-banner-content"]/text()').get(),
            'published': response.xpath('//span[@data-testid="vuln-published-on"]/text()').get(),
            'modified': response.xpath('//span[@data-testid="vuln-last-modified-on"]/text()').get(),
            'severity_cvss_2': response.xpath('//span[@class="severityDetail"]/a[@id="Cvss2CalculatorAnchor"]/text()').get(),
            'severity_cvss_3': response.xpath('//span[@class="severityDetail"]/a[@id="Cvss3NistCalculatorAnchor"]/text()').get(),
            'desc': response.xpath('//p[@data-testid="vuln-description"]/text()').get(),
            'further_details': response.xpath('//table[@data-testid="vuln-hyperlinks-table"]//a/@href').getall(),
            'cwe_links': response.xpath('//table[@data-testid="vuln-CWEs-table"]//a/@href').getall(),
        }
