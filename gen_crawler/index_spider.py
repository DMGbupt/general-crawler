# -*- coding: utf-8 -*-

"""以目录页面为入口的爬虫的抽象基类
"""

import urllib2
import cookielib
import time
from datetime import datetime
from datetime import timedelta
from abc import ABCMeta, abstractmethod

from scrapy import Spider
from scrapy import Request

from logs.crawler_logger import spider_logger

class IndexSpider(Spider):
    """子类只须实现抽象方法并提供self._search_url属性
    """

    __metaclass__ = ABCMeta  # 实现抽象基类

    # 目录页面第一页链接，并用{0}代替搜索词
    # 例如：_search_url = "http://news.search.hexun.com/news?key={0}&s=1&page=1&t=0&f=0"
    #_search_url = ""
    # 字符集，默认为utf8
    _char_set = "utf8"
    '''
    # 获取cookie
    _cookies=""
    '''

    def __init__(self,
                 config=None,
                 start_time=None,
                 end_time=None,
                 crawl_mode=None):
        """构造函数：用于向爬虫传递参数，请注意默认参数仅供测试使用
        :param config: 搜索词
        :param start_time: 仅爬取发布时间在start_time之后的网页，须保证目录页面中的网页以时间排序。
        :param end_time: 仅爬取发布时间在end_time之前的网页
        """
        # 搜索词列表，如果构造函数中config参数为None，则从self._config中读取
        if config:
            self.conf = config
        else:
            self.conf = self._config
        # 起始时间，默认值爬虫启动时间的100日前
        if start_time:
            self.from_time = start_time
        else:
            self.from_time = datetime.now()-timedelta(days=100)  # 默认值：100日前
        # 终止时间，默认值为当前时刻
        if end_time:
            self.end_time = end_time
        else:
            self.end_time = datetime.now()  # 默认值：当前时刻
        # crawl_mode
        if crawl_mode:
            self.crawl_mode = crawl_mode
        else:
            self.crawl_mode = 2


    def start_requests(self):
        query_count = 0
        conf = None
        try:
            for conf in self.conf:
                yield Request(conf['url'], callback = self.parse_index, meta = {'conf':conf})
                query_count += 1
        except Exception, e:
            spider_logger.error("Query No.{0} can't be encoded in {1}, because of {2}!"
                     .format(str(query_count), self.name, e))
 
    def parse_index(self, response):
        """处理目录页面，返回指向待爬取网页的Request列表
        """
        conf = response.meta['conf']
        requests = []
        page_list = self._get_result(response,conf)
        # 如果目录中没有内容，返回空列表
        if not page_list:
            return requests
        next_page = True  # 目录是否需要翻页
        # 逐条测试从目录中提取的网页列表
        for item in page_list:
            if isinstance(item, Request):  # 返回了新的Request
                requests.append(item)
                next_page = False
                break
            if item['publish_time']:
                if item['publish_time'] <= self.from_time:  # 网页发布时间早于self.from_time
                    next_page = False
                    break
            req = Request(item['crawl_url'], self.parse_page)
            # 传递已抽取信息
            req.meta["item"] = item
            requests.append(req)
        # 如需要翻页,添加下一页的Request;否则关闭生成器
        if next_page:
            requests.append(Request(self._next_result_page(response), callback = self.parse_index, meta = {'conf':conf}))
        return requests

    def parse_page(self, response):
        """处理一个网页
        """
        item = response.meta["item"]
        return self._finish_item(item, response)        

    @abstractmethod
    def _get_result(self, response):
        """从目录页面中获取网页列表
        :param response: 目录页面
        :return: crawlers.items.Base或其子类对象(必须抽取url和publish_time)的列表
        """
        pass

    @abstractmethod
    def _next_result_page(self, response):
        """抽取下一页目录的URL
        :param response: 当前处理的目录页面
        :return: 下一页目录的URL
        """
        pass

    @abstractmethod
    def _finish_item(self, item, response):
        """处理单个网页，抽取属性并填充item对象
        网页的属性可以从self._get_result()或本函数中提取
        :param item: self._get_result()中提取的item对象
        :param response: 当前处理网页
        :return: 处理完毕的item对象或新构造的Request对象
        """
        pass