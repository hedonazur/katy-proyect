# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class PdlScraperItem(Item):
    # define the fields for your item here like:
    codigo = Field()
    numero_proyecto = Field()
    periodo = Field()
    legislatura = Field()
    legislatura2 = Field()
    legislatura_name = Field()
    fecha_presentacion = Field()
    proponente = Field()
    grupo_parlamentario = Field()
    titulo = Field()
    titulo2 = Field()
    sumilla = Field()
    congresistas = Field()
    congresistas_ascii = Field()
    seguimiento_page = Field()
    short_url = Field()
    expediente = Field()
    iniciativas_agrupadas = Field()
    nombre_comision = Field()
    titulo_de_ley = Field()
    numero_de_ley = Field()
    pdf_url = Field()
    time_created = Field()
    time_edited = Field()
    seguimiento = Field()

