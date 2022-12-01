# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import logging
import pymongo
import sqlite3

class MongodbPipeline(object):

    collection_name = "computer_deals"
    
    # @classmethod
    # def from_crawler(cls,crawler):
    #     logging.warning(crawler.settings.get("MONGO_URI"))
    
    def open_spider(self,spider):
        self.client = pymongo.MongoClient("mongodb+srv://decodesaurav:decodesaurav2022@cluster0.w2ddzzi.mongodb.net/?retryWrites=true&w=majority")
        self.db = self.client["SLICKDEALS"]


    def close_spider(self,spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[self.collection_name].insert(item)
        return item

class SQLlitePipeline(object):

    #collection_name = "computer_deals"
    
    # @classmethod
    # def from_crawler(cls,crawler):
    #     logging.warning(crawler.settings.get("MONGO_URI"))
    
    def open_spider(self,spider):
        self.connection = sqlite3.connect("slickdeals.db")
        self.c = self.connection.cursor()
        try:
            self.c.execute('''
                CREATE TABLE computer_deals(
                    name TEXT,
                    link TEXT,
                    store_name TEXT,
                    price TEXT
                )

            ''')
            self.connection.commit()
        except sqlite3.OperationalError:
            pass

    def close_spider(self,spider):
        self.connection.close()

    def process_item(self, item, spider):
        #self.db[self.collection_name].insert(item)
        self.c.execute(''' 
            INSERT INTO computer_deals(name,link,store_name,price) VALUES(?,?,?,?)
        ''',(
            item.get('name'),
            item.get('link'),
            item.get('store_name'),
         item.get('price'),
        ))
        self.connection.commit()
        return item
