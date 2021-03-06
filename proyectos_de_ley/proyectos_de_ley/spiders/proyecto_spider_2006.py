# -*- coding: utf-8 -*-
import short_url
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from proyectos_de_ley.items import PdlScraperItem


LEGISLATURA = 2006


class ProyectoSpider2006(CrawlSpider):
    name = "proyecto_2006"
    allowed_domains = ["www2.congreso.gob.pe"]

    rules = (
        Rule(LinkExtractor(allow=('OpenDocument$',)), callback='parse_item'),
    )

    def __init__(self, *args, **kwargs):
        super(ProyectoSpider2006, self).__init__(*args, **kwargs)
        self.legislatura = LEGISLATURA

    def start_requests(self):
        base_url = (
            'http://www2.congreso.gob.pe/Sicr/TraDocEstProc/CLProLey2006.nsf/Numinversopa?OpenView&Start='
        )
        pages = range(1, 5000, 499)
        for page in pages:
            url = f'{base_url}{page}'
            yield scrapy.Request(url=url)

    def parse_item(self, response):
        self.log("this is the url: %s" % response.url)
        item = PdlScraperItem()
        item['codigo'] = ''
        item['legislatura'] = self.legislatura
        item['numero_proyecto'] = ''
        item['congresistas'] = ''
        item['titulo'] = ''
        item['short_url'] = ''
        item['fecha_presentacion'] = ''
        item['expediente'] = ''
        item['seguimiento_page'] = ''
        item['proponente'] = ''
        item['grupo_parlamentario'] = ''
        item['iniciativas_agrupadas'] = ''
        item['nombre_comision'] = ''
        item['titulo_de_ley'] = ''
        item['numero_de_ley'] = ''

        selectors = response.xpath("//input")
        for sel in selectors:
            attr_name = sel.xpath('@name').extract()[0]
            if attr_name == 'CodIni':
                item['codigo'] = sel.xpath('@value').extract()[0]
            if attr_name == 'CodIni_web_1':
                item['numero_proyecto'] = sel.xpath('@value').extract()[0]
            if attr_name == 'DesPerio':
                item['periodo'] = sel.xpath('@value').extract()[0]
            if attr_name == 'DesLegis':
                item['legislatura2'] = sel.xpath('@value').extract()[0]
            if attr_name == 'fechapre':
                item['fecha_presentacion'] = sel.xpath('@value').extract()[0]
            if attr_name == 'DesPropo':
                item['proponente'] = sel.xpath('@value').extract()[0]
            if attr_name == 'DesGrupParla':
                item['grupo_parlamentario'] = sel.xpath('@value').extract()[0]
            if attr_name == 'TitIni':
                item['titulo'] = sel.xpath('@value').extract()[0]
            if attr_name == 'Titulo':
                item['titulo2'] = sel.xpath('@value').extract()[0]
            if attr_name == 'SumIni':
                item['sumilla'] = sel.xpath('@value').extract()[0]
            if attr_name == 'NomCongre':
                item['congresistas'] = sel.xpath('@value').extract()[0]
            if attr_name == 'CodIniSecu':
                item['iniciativas_agrupadas'] = sel.xpath('@value').extract()[0]
            if attr_name == 'NumLey':
                item['numero_de_ley'] = sel.xpath('@value').extract()[0]
            if attr_name == 'TitLey':
                item['titulo_de_ley'] = sel.xpath('@value').extract()[0]
            if attr_name == 'NombreDeLaComision':
                item['nombre_comision'] = sel.xpath('@value').extract()[0]
        item['expediente'] = "http://www2.congreso.gob.pe/sicr/tradocestproc/Expvirt_2011.nsf/" \
                             "visbusqptramdoc1621/{}?opendocument".format(item['codigo'])
        item['seguimiento_page'] = response.url
        for sel in response.xpath('//td[@width="112"]'):
            if sel.xpath('font/text()').extract()[0] == 'Seguimiento':
                item['seguimiento'] = sel.xpath('following-sibling::*//text()').extract()
        item['short_url'] = self.create_shorturl(item['codigo'])
        return item

    def create_shorturl(self, codigo):
        """
        Use "legislatura" and codigo to build a short url.
        :param codigo: Code for Proyecto de ley "03774"
        :return: 4aw8ym
        """
        mystring = "%s%s" % (self.legislatura, codigo)
        url = short_url.encode_url(int(mystring))
        return url
