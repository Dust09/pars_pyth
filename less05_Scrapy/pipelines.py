# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient

class JobparserPipeline(object):
    def __init__(self):
        client = MongoClient('localhost',27017)
        self.mongo_base = client.vacancy228


    def process_item(self, item, spider):
        if spider.name == 'hhru':

            res = "з/п не указана"
            sal_f = "".join(item['salary'])
            name = item['name']
            if 'от ' in item['salary'] and 'до' in item['salary'] and len(item['salary']) > 3:
                res = {'vacancy':name,'min':item['salary'][1].replace('\xa0',' '),'max':item['salary'][3].replace('\xa0',' '),'link':item['link'],'site':item['site']}
            elif 'от' in sal_f and 'до' not in item['salary']:
                res = {'vacancy':name,'min':item['salary'][1].replace('\xa0',' '),'max':item['salary'][1].replace('\xa0',' '),'link':item['link'],'site':item['site']}
            elif "до" in sal_f:
                res = {'vacancy':name,"min": "не указано", "max": item['salary'][1].replace(u'\xa0', ' '),'link':item['link'],'site':item['site']}

            collection = self.mongo_base[spider.name]
            collection.insert_one(res)
        else:
            #spider.name == 'superjob':
            res ='по договоренности'
            sal_f = ''.join(item['salary'])
            name = item['name']

            if '—' in sal_f and len(item['salary'])>5  :
                res = {'vacancy':name,'min':item['salary'][0].replace('\xa0',' '), 'max':item['salary'][4].replace('\xa0',' '),'link':item['link'],'site':item['site']}
            elif '₽' in item['salary']:
                res = {'vacancy':name,'min':item['salary'][0].replace('\xa0',' '),'max':item['salary'][0].replace('\xa0',' '),'link':item['link'],'site':item['site']}
            elif '' in sal_f and 'None' not in item['name']:
                res = {'vacancy':name,'min':'По договоренности','max':'по договоренности','link':item['link'],'site':item['site']}
            collection = self.mongo_base[spider.name]
            collection.insert_one(res)

            print(res)


        return item
