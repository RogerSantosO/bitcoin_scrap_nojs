from requests import request
import scrapy


class BitcoinSpider(scrapy.Spider):
    name = 'bitcoin'
    allowed_domains = ['finance.yahoo.com']
    start_urls = ['https://finance.yahoo.com/quote/BTC-USD/history/']

    #to make a csv file, comment this parse and rename "parse2" to "parse"
    def parse(self, response):
        yield {
            'Coin': response.xpath('//div[@class="D(ib) "]/h1/text()').get(),
            'Price Now': response.xpath('//div[@class="D(ib) Mend(20px)"]/fin-streamer/text()').get()
        }
        yield scrapy.Request('https://finance.yahoo.com/quote/BTC-USD/history/',callback=self.parse2)

    
    def parse2(self, response):
        history = response.xpath('//tbody/tr[@class="BdT Bdc($seperatorColor) Ta(end) Fz(s) Whs(nw)"]')
        for data in history:
            yield {
                'Date': data.xpath('(.//span)[1]/text()').get(),
                'Open': data.xpath('(.//span)[2]/text()').get(),
                'High': data.xpath('(.//span)[3]/text()').get(),
                'Low': data.xpath('(.//span)[4]/text()').get(),
                'Close': data.xpath('(.//span)[5]/text()').get(),
                'Adjusted Close': data.xpath('(.//span)[6]/text()').get(),
                'Volume': data.xpath('(.//span)[7]/text()').get()
            }
            