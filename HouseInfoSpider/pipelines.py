# -*- coding: utf-8 -*-


import pymongo
from items import HouseInfoItem


class HouseinfospiderPipeline(object):
    def process_item(self, item, spider):
        return item


class MongoPipeline(object):
	# 集合名
    hp_collection_name = 'house_info'

	# 初始化该数据库
    def __init__(self,mongo_uri,mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod		# 指定该方法为类方法
    def from_crawler(cls,crawler):
        return cls(
            mongo_uri = crawler.settings.get('MONGO_URI'),
            mongo_db = crawler.settings.get('MONGO_DATABASE','items')
        )

	# 数据库连接
    def open_spider(self,spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

	# 数据库关闭
    def close_spider(self,spider):
        self.client.close()

    # 将数据存入到数据库中
    def process_item(self,item,spider):
        if isinstance(item, HouseInfoItem):
            # key_index = item['url']
            # if not self.db[self.hp_collection_name].find({'url':key_index}).count():
            self.db[self.hp_collection_name].insert(dict(item))           #存入数据库原始数据
        return item