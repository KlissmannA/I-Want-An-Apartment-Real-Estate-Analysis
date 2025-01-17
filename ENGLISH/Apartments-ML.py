from scrapy.item import Field

from scrapy.item import Item

from scrapy.spiders import CrawlSpider, Rule

from scrapy.selector import Selector

from scrapy.linkextractors import LinkExtractor

from scrapy.loader import ItemLoader

from itemloaders.processors import MapCompose

from scrapy.crawler import CrawlerProcess


class Apartament(Item):

    title = Field()

    cost = Field()

    url = Field()

    rooms = Field()

    bathrooms = Field()

    rootmeters = Field()

    description = Field()

    salesperson = Field()

    address = Field()

    id = Field()


class DetailApartments(CrawlSpider):

    name = 'MercadoLibreBqto'

    custom_settings = {

        'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',

        'FEED_FORMAT': 'json',

        'FEED_URI': 'mercadolibrebqto2.json',

        'CLOSESPIDER_PAGECOUNT': 100,

        'FEED_EXPORT_ENCODING': 'utf-8'

    }


    download_delay = 1


    allowed_domains = ['listado.mercadolibre.com.ve', 'apartamento.mercadolibre.com.ve']


    start_urls = ['https://listado.mercadolibre.com.ve/inmuebles/apartamentos-barquisimeto_NoIndex_True']


    rules = (

        Rule(

            LinkExtractor(allow = r'_NoIndex_True'),

            follow = True

        ),

        Rule(

            LinkExtractor(allow = r'/MLV-'),

            follow = True,

            callback="item_main_page"

        ),

       

    )


    def __init__(self, *args, **kwargs):

        super(DetailApartments, self).__init__(*args, **kwargs)

        self.id = 0


    def item_main_page(self,response):

        item = ItemLoader(Apartament(),response)

        self.id += 1

        item.add_value('id', self.id)

        item.add_xpath('title', './/h1/text()')

        item.add_xpath('url', './/h2/a/@href')

        item.add_xpath('description', './/div[@class="ui-pdp-description"]//p/text()')

        item.add_xpath('salesperson', './/div[@class ="ui-vip-profile-info"]//h3/text()')

        item.add_xpath('bathrooms', './/div[@class ="ui-pdp-highlighted-specs-res"]/div[3]/span/text()')

        item.add_xpath('rootmeters', './/div[@class ="ui-pdp-highlighted-specs-res"]/div[1]/span/text()')

        item.add_xpath('rooms', './/div[@class ="ui-pdp-highlighted-specs-res"]/div[2]/span/text()')

        item.add_xpath('cost', './/span[@class="andes-money-amount ui-pdp-price__part andes-money-amount--cents-superscript andes-money-amount--compact"]//span[@class="andes-money-amount__fraction"]/text()')

        item.add_xpath('address', './/div[@class="ui-pdp-media ui-vip-location__subtitle ui-pdp-color--BLACK"]//p/text()')


        yield item.load_item()



process = CrawlerProcess()

process.crawl(DetailApartments)

process.start()
