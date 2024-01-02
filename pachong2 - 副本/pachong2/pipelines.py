import pymongo
from scrapy.exceptions import DropItem

class MongoDBPipeline:
    collection_name = 'pachong'  # 更新为您的MongoDB集合名称

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        # 转换价格字段为实际的数字
        if '价格' in item:
            price = item['价格']
            try:
                # 判断价格是否包含"万"单位
                if '万' in price:
                    # 去除价格中的"万"并转换为实际数字
                    price_value = float(price.replace('万', ''))
                    # 将价格乘以一万，得到实际的价格
                    item['价格'] = int(price_value * 10000)
                else:
                    # 如果价格没有单位"万"，将其转换为整数
                    item['价格'] = int(float(price))
            except ValueError:
                raise DropItem("Invalid price format in %s" % item)

        if item.get('价格') is None:
            raise DropItem("Missing price in %s" % item)

        # 插入数据到 MongoDB
        self.db[self.collection_name].insert_one(dict(item))
        return item
