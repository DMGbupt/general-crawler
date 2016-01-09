# -*- coding: utf-8 -*-

"""
已设置失败重连次数为3次。
"""

import re
from datetime import datetime
import urllib

from scrapy import Request

from gen_crawler.items import Cpca1
from gen_crawler.index_spider import IndexSpider
from gen_crawler.utils.html_formatter import HtmlFormatter
from gen_crawler.configs.cpca1_config import CONF
from gen_crawler.logs.crawler_logger import spider_logger


class Cpca1News(IndexSpider):

    name = "cpca1"
    _config = CONF

    def _get_result(self, response, config):
        rel = []
        conf = config
        results = response.xpath("//a[@class='tittleoyy']")
        if not results:
            spider_logger.error("Can't get url lists from %s" % conf['url'])
            return
        # 提取搜索结果
        for ul in results:
            item = Cpca1()
            # 从搜索结果页抽取信息
            item['crawl_url'] = "http://www.cpca1.org/" + ul.xpath("./@href").extract()[0]
            item['title'] = ul.xpath("./text()").extract()
            item['keyword'] = conf['keyword']
            item['publish_time'] = None
            rel.append(item)
        return rel

    def _next_result_page(self, response):
        attr = re.split("=", response.url)
        page = int(attr[-1])
        pages = response.xpath(
            "//div[@class='Page']/table/tr/td[last()]/a[last()]/@href").extract()[0]
        if not pages:
            spider_logger.info("%s is the end of index page!" % response.url)
            return
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
        item['crawl_website'] = u"全国汽车市场研究会"
        item['source_website'] = item['crawl_website']
        item['atc'] = 0
        Publishtime = response.xpath(
            "//td[@class='weizhilinkaa']/div[@align='center']/text()").extract()[2]
        publish_time = Publishtime.split(u'：')[-1]
        item['publish_time'] = datetime.strptime(publish_time.replace(
            u'年', "-").replace(u'月', "-").replace(u'日', "").strip()+" 00:00:00", "%Y-%m-%d %H:%M:%S")
        # content
        content = response.xpath("//td[@valign='top'][@class='weizhilinkaa']").extract()
        item['content'] = HtmlFormatter.format_content(content[1])
        # image
        item['image_urls'] = []
        for img_url in response.xpath("//td[@valign='top'][@class='weizhilinkaa']//img/@src").extract():
            if re.match("http.*", img_url):
                item['image_urls'].append(img_url)
            else:
                img_url = "http://www.cpca1.org"+img_url
                item['image_urls'].append(img_url)
        return item
