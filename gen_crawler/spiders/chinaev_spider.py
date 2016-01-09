# -*- coding: utf-8 -*-

"""
已设置失败重连次数为3次。
"""

import re
from datetime import datetime
import urllib

from scrapy import Request

from gen_crawler.items import Chinaev
from gen_crawler.index_spider import IndexSpider
from gen_crawler.utils.html_formatter import HtmlFormatter
from gen_crawler.configs.chinaev_config import CONF
from gen_crawler.logs.crawler_logger import spider_logger

class ChinaevNews(IndexSpider):

    name = "chinaev"
    _config = CONF

    def _get_result(self, response, config):
        rel = []
        conf = config
        results = response.xpath("//div[@class='ui-box-content newslist']/ul/li[not(contains(@class,'dotted-line'))]")
        if not results:
            spider_logger.error("Can't get url lists from %s" % conf['url'])
            return
        # 提取搜索结果
        for ul in results:
            item = Chinaev()
            # 从搜索结果页抽取信息
            item['crawl_url'] = "http://www.chinaev.org/DisplayView/Normal/News/"+ul.xpath("./a/@href").extract()[0]
            item['title'] = ul.xpath("./a/text()").extract()[0]
            item['keyword'] = conf['keyword']
            publishtime = ul.xpath("./span/text()").extract()[0]
            item['publish_time'] = datetime.strptime(publishtime, "%Y-%m-%d %H:%M:%S")
            rel.append(item)
        return rel

    def _next_result_page(self, response):
        attr = re.split("=", response.url)
        page = int(attr[-1])
        pages = response.xpath("//div[@class='ep-pages']/a[last()]/@href").extract()[0]
        maxpage = int(re.split("=", pages)[-1])
        crawlpage = 3
        if page < (maxpage if self.crawl_mode == 1 else(crawlpage if crawlpage<maxpage else maxpage)):
            page += 1
            attr[-1] = str(page)
        else:
            spider_logger.info("Get last index page: %s" % response.url)
            return 
        return "=".join(attr)

    def _finish_item(self, item, response):
        # 继续提取信息
        item['crawl_website'] = u"节能与新能源汽车网"
        item['atc'] = 0
        item['source_website'] = response.xpath("//span[@class='comefrom']/text()").extract()[0]
        # content
        content = response.xpath("//div[@class='content']").extract()
        item['content'] = HtmlFormatter.format_content(content[0])
        # image
        item['image_urls'] = []
        for img_url in response.xpath("//div[@class='content']//img/@src").extract():
            if re.match("http.*", img_url):
                item['image_urls'].append(img_url)
            else:
                img_url = "http://www.chinaev.org"+img_url
                item['image_urls'].append(img_url)                
        return item
