
import scrapy
import pymongo


class Fivei5jSpider(scrapy.Spider):
    name = 'woaiwojia'
    allowed_domains = ['bj.5i5j.com']
    start_urls = ['https://bj.5i5j.com/ershoufang/']

    custom_settings = {
        'DEFAULT_REQUEST_HEADERS': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36',
            'Referer': 'https://bj.5i5j.com/'
        },
        'FEEDS': {
            'items.json': {
                'format': 'json',
                'overwrite': True,
                'indent': 4,
                'fields': None,
                'include_links': True,
            }
        }
    }
    # 添加MongoDB配置
    mongo_uri = 'mongodb://localhost:27017/'  # MongoDB URI
    mongo_db = 'pachong'  # MongoDB数据库名称
    mongo_collection = 'pachong'  # MongoDB集合名称

    def __init__(self, *args, **kwargs):
        super(Fivei5jSpider, self).__init__(*args, **kwargs)
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        self.collection = self.db[self.mongo_collection]

    def close(self, reason):
        self.client.close()
        super(Fivei5jSpider, self).close(self, reason)

    def parse(self, response):
        base_url = 'https://bj.5i5j.com'  # 基础URL

        # 定位具有特定类名的元素并提取链接
        for element in response.css('.listTit'):
            relative_link = element.css('a::attr(href)').get()
            if relative_link:
                # 构建完整的链接
                full_link = base_url + relative_link
                yield scrapy.Request(full_link, callback=self.parse_house)

        # 获取下一页链接
        next_page = response.css('a.cPage::attr(href)').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def parse_house(self, response):
        house_name = response.xpath('/html/body/div[6]/div[1]/div[1]/h1/text()').get()
        price = response.xpath('/html/body/div[6]/div[2]/div[2]/div[1]/div[1]/div[1]/span/text()').get()
        agent_name = response.xpath('/html/body/div[6]/div[2]/div[2]/div[3]/ul/li[2]/h3/a/text()').get()

        house_link = response.url  # 获取当前页面的链接

        # 提取基础属性信息和交易属性信息...
        # 提取基础属性信息
        basic_attributes = {
            '房屋户型': response.xpath(
                '/html/body/div[6]/div[3]/div[3]//ul/li[label/text()="房屋户型"]/span/text()').get(),
            '所在楼层': response.xpath(
                '/html/body/div[6]/div[3]/div[3]//ul/li[label/text()="所在楼层"]/span/text()').get(),
            '建筑面积': response.xpath(
                '/html/body/div[6]/div[3]/div[3]//ul/li[label/text()="建筑面积"]/span/text()').get(),
            '户型结构': response.xpath(
                '/html/body/div[6]/div[3]/div[3]//ul/li[label/text()="户型结构"]/span/text()').get(),
            '套内面积': response.xpath(
                '/html/body/div[6]/div[3]/div[3]//ul/li[label/text()="套内面积"]/span/text()').get(),
            '建筑类型': response.xpath(
                '/html/body/div[6]/div[3]/div[3]//ul/li[label/text()="建筑类型"]/span/text()').get(),
            '房屋朝向': response.xpath(
                '/html/body/div[6]/div[3]/div[3]//ul/li[label/text()="房屋朝向"]/span/text()').get(),
            '建筑结构': response.xpath(
                '/html/body/div[6]/div[3]/div[3]//ul/li[label/text()="建筑结构"]/span/text()').get(),
            '装修情况': response.xpath(
                '/html/body/div[6]/div[3]/div[3]//ul/li[label/text()="装修情况"]/span/text()').get(),
            '供暖方式': response.xpath(
                '/html/body/div[6]/div[3]/div[3]//ul/li[label/text()="供暖方式"]/span/text()').get(),
            '配备电梯': response.xpath(
                '/html/body/div[6]/div[3]/div[3]//ul/li[label/text()="配备电梯"]/span/text()').get()
        }

        # 提取交易属性信息
        transaction_attributes = {
            '发布时间': response.xpath(
                '/html/body/div[6]/div[3]/div[3]//ul/li[label/text()="发布时间"]/span/text()').get(),
            '建成年代': response.xpath(
                '/html/body/div[6]/div[3]/div[3]//ul/li[label/text()="建成年代"]/span[1]/text()').get(),
            '产权性质': response.xpath(
                '/html/body/div[6]/div[3]/div[3]//ul/li[label/text()="产权性质"]/span/text()').get(),
            '规划用途': response.xpath(
                '/html/body/div[6]/div[3]/div[3]//ul/li[label/text()="规划用途"]/span/text()').get(),
            '上次交易': response.xpath(
                '/html/body/div[6]/div[3]/div[3]//ul/li[label/text()="上次交易"]/span/text()').get(),
            '购房年限': response.xpath(
                '/html/body/div[6]/div[3]/div[3]//ul/li[label/text()="购房年限"]/span/text()').get(),
            '共有情况': response.xpath(
                '/html/body/div[6]/div[3]/div[3]//ul/li[label/text()="共有情况"]/span/text()').get(),
            '抵押情况': response.xpath(
                '/html/body/div[6]/div[3]/div[3]//ul/li[label/text()="抵押情况"]/span/text()').get(),
            '房本备件': response.xpath(
                '/html/body/div[6]/div[3]/div[3]//ul/li[label/text()="房本备件"]/span/text()').get()
        }
        yield {
            '房屋名称': house_name.strip() if house_name else None,
            '价格': price.strip() if price else None,
            '经纪人姓名': agent_name.strip() if agent_name else None,
            '房屋链接': house_link,  # 将房屋链接包含在输出中
            '基础属性信息': basic_attributes,
            '交易属性信息': transaction_attributes
        }
        # 将数据存储到MongoDB
        data_to_insert = {
            '房屋名称': house_name.strip() if house_name else None,
            '价格': price.strip() if price else None,
            '经纪人姓名': agent_name.strip() if agent_name else None,
            '房屋链接': house_link,  # 保留房屋链接在输出中
            '基础属性信息': basic_attributes,
            '交易属性信息': transaction_attributes
            # 根据需要添加其他字段
        }

        # 插入数据到MongoDB集合中
        self.collection.insert_one(data_to_insert)

        yield data_to_insert

# 运行Spider
# scrapy crawl woaiwojia -o output.json  # 您也可以将爬取的数据输出到文件中