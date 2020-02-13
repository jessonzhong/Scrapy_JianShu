# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from jianshu_spider.items import JianshuSpiderItem

class JsSpider(CrawlSpider):
    name = 'js'
    allowed_domains = ['jianshu.com']
    start_urls = ['http://jianshu.com/']

    rules = (
        Rule(LinkExtractor(allow=r'.*/p/[0-9a-z]{12}'), callback='parse_detail', follow=True),
    )

    def parse_detial(self, response):
        title = response.xpath('//h1[@class="title"]/text()').extract_first('')  # 提取标题
        avatar = response.xpath('//a[@class="avatar"]/img/@src').extract_first('')  # 提取头像
        author = response.xpath('//span[@class="name"]/a/text()').extract_first('')  # 提取作者
        publish_time = response.xpath('//span[@class="publish-time"]/text()').extract_first('')  # 提取发布时间
        content = response.xpath('//div[@class="show-content"]').get()  # 提取文章内容
        # 提取文章ip
        process_url = response.url.split('?')[0]  # 以问号分割取前一部分
        article_id = process_url.split('/')[-1]  # 以 ‘/’ 分割获取最后一个字符串即为文章的id
        origin_url = response.url

        item = JianshuSpiderItem(title=title, avatar=avatar, author=author, publish_time=publish_time,
                                 content=content, article_id=article_id, origin_url=origin_url)
        yield item