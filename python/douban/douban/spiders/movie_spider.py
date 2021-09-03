#这里定义爬虫事件需要的具体的逻辑代码
#   ↑   定义了默认的编码译码方式为utf-8
# -*- coding: utf-8 -*-
import scrapy
from ..items import DoubanItem

class MovieSpiderSpider(scrapy.Spider):
    #爬虫的名字，每个爬虫都有自己的特有的名字
    name = 'movie_spider'
    #允许的域名，也就是头域名，在这个域名下面有很多字域名
    allowed_domains = ['movie.douban.com']
    #入口URL，也就是最后需要爬取信息的URL地址
    start_urls = ['https://movie.douban.com/top250']

    #定义parse()函数，用于处理每一个Request返回的Response，self代表自身这个spider爬虫，response即每个xpath
    def parse(self, response):
        #选取网页检查中article大类以及其下面的grid_view小类，注意div class和ol class要区分出来
        movie_list = response.xpath(
            "//div[@class='article']//ol[@class='grid_view']/li")

        # 循环电影的条目，子条目存储到i_item列表中
        for i_item in movie_list:
            # 导入DoubanItem，进行数据解析,并将其中的数据存到新的数组douban_item中
            douban_item = DoubanItem()

            #定义序列号的数据范围，也就是排名的数字
            douban_item['serial_num'] = i_item.xpath(
                ".//div[@class='item']//em/text()").extract_first()

            #定义电影名称的数据范围
            douban_item['movie_name'] = i_item.xpath(
                ".//div[@class='info']//div[@class='hd']/a/span[1]/text()").extract_first()

            # 如果文件有多行进行解析，内容有多行的时候，需要进行分割再使用，这里介绍板块肯定有很多行
            content = i_item.xpath(
                ".//div[@class='info']//div[@class='bd']/p[1]/text()").extract()
            #定义一个i_content列表用来保存content中的数据
            for i_content in content:
                #用"sep".join(seq)语法来以特定的字符连接新的字符串，sep即为分隔符，可以是空，seq即为要连接的序列，字符串，元组，字典等
                #使用split()函数，通过指定分隔符对字符串进行切片，如果参数 num 有指定值，则分隔 num+1 个子字符串
                content_s = "".join(i_content.split())
                douban_item['introduce'] = content_s

            #星级数据
            douban_item['star'] = i_item.xpath(
                ".//span[@class='rating_num']/text()").extract_first()

            #评价数据
            douban_item['evaluate'] = i_item.xpath(
                ".//div[@class='star']//span[4]/text()").extract_first()

            #介绍数据
            douban_item['describe'] = i_item.xpath(
                ".//p[@class='quote']/span/text()").extract_first()

            #输出douban_item列表
            print(douban_item)
            #返回数据
            yield douban_item

        # 解析下一页，取后一页的XPATH，放到next_link列表里面
        next_link = response.xpath(
            "//span[@class='next']/link/@href").extract()
        if next_link:
            next_link = next_link[0]
            #当取得到下一页的时候，重新执行操作，用request()函数进行
            #请求下一页地址后，回调函数，self.parse
            yield scrapy.Request(
                "https://movie.douban.com/top250" + next_link, callback=self.parse)
