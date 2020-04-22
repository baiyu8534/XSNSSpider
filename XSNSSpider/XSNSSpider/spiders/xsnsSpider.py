# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

import re


class XsnsspiderSpider(CrawlSpider):
    name = 'xsnsSpider'
    allowed_domains = ['www.xsnvshen.com']
    start_urls = ['https://www.xsnvshen.com/album/hd/?p=1']

    rules = (                     # /album/hd/?p=2
        Rule(LinkExtractor(allow=r'/album/hd/\?p\=\d+'), callback='parse_page', follow=True),
    )

    def parse_page(self, response):
        print("parse_page")
        li_list = response.xpath('//div[@class="index_listc"]//li')
        for li in li_list:
            item = {}
            item["title"] = li.xpath("./a/@title").extract_first()
            item["url"] = li.xpath("./a/@href").extract_first()
            item["id"] =  item["url"].split("/")[-1]
            item["pic_count"] = li.xpath(".//span[@class='num']/text()").extract_first()
            item["cover_img_url"] = li.xpath(".//img[@class='lazy']/@src").extract_first()
            img_path = item["cover_img_url"]
            img_path = re.findall("album(.*?)cover", img_path)[0]
            item["pic_urls"] = ["http://img.xsnvshen.com/album{}{}.jpg".format(img_path, str(i).zfill(3))
                                for i in range(0, int(item["pic_count"]))]
            yield item
