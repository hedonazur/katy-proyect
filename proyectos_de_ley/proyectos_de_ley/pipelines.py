# -*- coding: utf-8 -*-
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from copy import copy, deepcopy
from datetime import datetime
import pytz
import re
import six
import unicodedata
import logging

log = logging.getLogger()


def convert_to_ascii(my_string):
    return unicodedata.normalize(
        'NFKD',
        my_string,
    ).encode('ascii', 'ignore').decode('utf-8')


class PdlScraperPipeline(object):
    def process_item(self, item, spider):
        if 'proyecto' in str(spider.name):
            item['fecha_presentacion'] = self.fix_date(item['fecha_presentacion'])
            item['congresistas'] = self.parse_names(item['congresistas'])
            item['congresistas_ascii'] = convert_to_ascii(item['congresistas'])
            item['iniciativas_agrupadas'] = self.parse_iniciativas(item['iniciativas_agrupadas'])
            item['time_created'] = datetime.utcnow().replace(tzinfo=pytz.utc)
            item['time_edited'] = datetime.utcnow().replace(tzinfo=pytz.utc)
            return item
        return item

    def fix_date(self, string):
        """
        Takes an string date from Proyecto and converts it to Date object.
        :param string: "08/28/2014"
        :return: date(2014, 08, 28)
        """
        try:
            mydate = datetime.date(datetime.strptime(string, '%d/%m/%Y'))
        except ValueError:
            # mydate = datetime.date(datetime.strptime(string, '%m/%d/%Y'))
            log.debug(f"fecha_presentacion was not in the right format. {string}")
            string = "1970-01-01"
            mydate = datetime.date(datetime.strptime(string, '%Y-%m-%d'))
        return mydate

    def parse_names(self, string):
        """
        :param string: Person names separated by commas.
        :return: String of person names separated by colons and family names
                 separated from given names by commas.
        """
        names = ""
        for i in string.split(","):
            i = re.sub("\s{2}", ", ", i)
            names += i + "; "
        names = re.sub(";\s$", "", names)
        return names

    def parse_iniciativas(self, string):
        """
        :param string:
        :return: list of iniciativas
        """
        if type(string) == list:
            return ''

        if string.strip() == '':
            return ''

        iniciativas = string.split(",")
        iniciativas_stripped = [i.strip() for i in iniciativas]
        return iniciativas_stripped

