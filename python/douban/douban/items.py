# Define here the models for your scraped items
#这里定义需要抓取的数据项
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DoubanItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    # 爬取的序列号
    serial_num = scrapy.Field();
    # 电影名
    movie_name = scrapy.Field();
    # 介绍
    introduce = scrapy.Field();
    # 星级
    star = scrapy.Field();
    # 评价数
    evaluate = scrapy.Field();
    # 描述
    describe = scrapy.Field();
    pass
