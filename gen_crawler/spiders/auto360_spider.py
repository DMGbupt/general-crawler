# -*- coding: utf-8 -*-

"""
已设置失败重连次数为3次。
"""

import re
from datetime import datetime
import urllib

from scrapy import Request

from gen_crawler.items import Auto360
from gen_crawler.index_spider import IndexSpider
from gen_crawler.utils.html_formatter import HtmlFormatter
from gen_crawler.configs.auto360_config import CONF
from gen_crawler.logs.crawler_logger import spider_logger


class Auto360News(IndexSpider):

    name = "auto360"
    _config = CONF

    def _get_result(self, response, config):
        rel = []
        conf = config
        results = response.xpath("//div[@class='news_list']/ul")
        if not results:
            spider_logger.error("Can't get url lists from %s" % conf['url'])
            return
        # 提取搜索结果
        for ul in results:
            item = Auto360()
            # 从搜索结果页抽取信息
            item['crawl_url'] = ul.xpath("./span[@class='list_title']/a/@href").extract()[0]
            item['title'] = ul.xpath("./span[@class='list_title']/a/text()").extract()
            item['keyword'] = conf['keyword']
            publishtime = ul.xpath("./span[@class='date']/text()").extract()[0]
            try:
                item['publish_time'] = datetime.strptime(publishtime, "%Y-%m-%d %H:%M:%S")
            except Exception, e:
                spider_logger.warning("Convert date format in %s" % item['crawl_url'])
                item['publish_time'] = datetime.strptime(publishtime+" 00:00:00", "%Y-%m-%d %H:%M:%S") 
            rel.append(item)
        return rel

    def _next_result_page(self, response):
        attr = re.split("_|.html", response.url)
        page = int(attr[-2])
        pages = response.xpath("//ul[@class='pagination']/a[last()]/@href").extract()[0]
        maxpage = int(re.split("_|.html", pages)[-2])
        crawlpage = 3
        if page < (maxpage if self.crawl_mode == 1 else(crawlpage if crawlpage<maxpage else maxpage)):
            page += 1
            attr[-2] = str(page)
        else:
            spider_logger.error("Can't get next page from %s" % response.url)
            return 
        return "_".join(attr[:-1])+".html"

    def _finish_item(self, item, response):
        # 继续提取信息
        item['crawl_website'] = u"中国汽车资讯中心网"
        item['atc'] = 0
        item['source_website'] = response.xpath("//span[@class='article-source']/text()").extract()
        # content
        content = response.xpath("//div[@class='content']").extract()
        item['content'] = HtmlFormatter.format_content(content[0])
        # image
        item['image_urls'] = []
        for img_url in response.xpath("//div[@class='content']//img/@src").extract():
            if re.match("http.*", img_url):
                item['image_urls'].append(img_url)
        return item
