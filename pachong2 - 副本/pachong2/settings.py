BOT_NAME = "pachong2"

SPIDER_MODULES = ["pachong2.spiders"]
NEWSPIDER_MODULE = "pachong2.spiders"

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"


MONGO_URI = 'mongodb://localhost:27017/'  # 更新为您的MongoDB URI
MONGO_DATABASE = 'pachong'  # 更新为您的MongoDB数据库名称
