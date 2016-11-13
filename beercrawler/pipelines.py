# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy import signals
from scrapy.contrib.exporter import CsvItemExporter
import json


class CSVPipeline(object):

    # def __init__(self):
    #     self.files = {}
    #
    # @classmethod
    # def from_crawler(cls, crawler):
    #     pipeline = cls()
    #     crawler.signals.connect(pipeline.open_spider, signals.spider_opened)
    #     crawler.signals.connect(pipeline.close_spider, signals.spider_closed)
    #     return pipeline
    #
    # def open_spider(self, spider):
    #     file = open(spider.name + '.csv', 'wb')
    #     self.files[spider] = file
    #     self.exporter = CsvItemExporter(file)
    #     self.exporter.fields_to_export = ['id', 'brewery', 'name', 'style', 'abv', 'rating', 'state', 'country']
    #     self.exporter.start_exporting()
    #
    # def close_spider(self, spider):
    #     self.exporter.finish_exporting()
    #     file = self.files.pop(spider)
    #     file.close()
    #
    # def process_item(self, item, spider):
    #     self.exporter.export_item(item)
    #     return item

    def __init__(self):
        self.files = {}

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        file = open(spider.name + '.csv', 'w+b')
        self.files[spider] = file
        self.exporter = CsvItemExporter(file)
        self.exporter.fields_to_export = ['id', 'brewery', 'name', 'style', 'abv', 'rating', 'state', 'country', 'breweryoriginal']
        self.exporter.start_exporting()

    def spider_closed(self, spider):
        self.exporter.finish_exporting()
        file = self.files.pop(spider)
        file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item

# class HtmlFilePipeline(object):
#     def process_item(self, item, spider):
#         print item['url']
#         file_name = hashlib.sha224(item['url']).hexdigest()
#         with open('files/%s.html' % file_name, 'w+b') as f:
#             f.write(item['html'])
#         return item

class JsonWriterPipeline(object):

    def open_spider(self, spider):
        self.file = open('untappd.json', 'wb')

    def close_spider(self, spider):
        self.file.close()

    def proces_item(self, item, spider):
        line = json.dumps(dict(item)) + '\n'
        self.file.write(line)
        return item

class BeercrawlerPipeline(object):
    def process_item(self, item, spider):
        return item
