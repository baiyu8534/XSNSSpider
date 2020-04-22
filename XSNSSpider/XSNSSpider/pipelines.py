# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import datetime
from pymongo import MongoClient
import redis
from scrapy.pipelines.images import ImagesPipeline
from scrapy import Request
import re

client = MongoClient("localhost", 27017)
collection = client["XSNS"]["XSNS_image"]

spider_name = 'xsnsSpider'
redis_conn = redis.Redis(host='localhost', port=6379, db=0)
redis_json_key = "down_item_json"
# 用自带的图片去重
redis_img_key = "down_img"


def reset_file_path(file_path):
    r_file_path = re.sub('[\/:*?"<>|]', '-', file_path)  # 去掉非法字符
    return r_file_path


class XsnsspiderPipeline(object):

    def process_item(self, item, spider):
        added = redis_conn.sadd(spider_name + ":" + str(redis_json_key), item["id"])
        if added == 1:
            item["catch_time"] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            collection.insert(dict(item))
            print("保存-->>" + item["title"])
        return item


class DownloadImage(ImagesPipeline):

    def get_media_requests(self, item, info):
        # 这个方法是在发送下载请求之前调用的，其实这个方法本身就是去发送下载请求的

        dir_name = item["title"]
        print(dir_name)
        return [Request(url, meta={'dir_name': dir_name}) for url in item["pic_urls"]]

    def file_path(self, request, response=None, info=None):
        # 这个方法是在图片将要被存储的时候调用，来获取这个图片存储的路径
        # added = redis_conn.sadd(spider_name + ":" + str(redis_img_key), item["id"])
        # if added == 1:
        print("下载完毕-->" + request.url)
        dir_name = request.meta['dir_name']
        file_name = request.url.split('/')[-1]
        image_path = reset_file_path(dir_name) + "/" + reset_file_path(file_name)
        return image_path
