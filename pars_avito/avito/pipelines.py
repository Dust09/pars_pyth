# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
from scrapy.pipelines.images import ImagesPipeline
import os

from pymongo import MongoClient

class DataBaseline(object):
    def __init__(self):
        client = MongoClient('localhost',27017)
        self.mongo_base = client.avito_photo

    def process_item(self, item, spider):
        item['price'] = int(item['price'][0].replace(' ',''))
        res =[]
        value=[]
        key=[]
        test =[]
        select=[]
        for i in item['params']:
            if len(i)>3:
                test.append(i)
            else:
                pass
        for i in test:
            if ':' not in i:
                value1 =i.replace('\xa0','')
                value.append(value1)
            else:
                pass
            if ':' in i:
                key1 = i
            else:
                pass
        for i,z in zip(key,value):
            select.append({i:z})
            item['params']=select
        collection = self.mongo_base[spider.name]
        collection.insert_one(item)
        return item

class AvitoPhotosPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['photos']:
            for img in item['photos']:
                try:
                    yield scrapy.Request(img) ##(f'http://{img}')
                except Exception as e:
                    print('error')
        return item

    def item_completed(self, results, item, info):
        if results:
            item['photos'] = [itm[1] for itm in results if itm[0]]
        return item


