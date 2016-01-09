# -*- coding: utf-8 -*-

"""
已设置失败重连次数为3次。
"""

import re
from datetime import datetime
import urllib

from scrapy import Request

from gen_crawler.items import Caam
from gen_crawler.index_spider import IndexSpider
from gen_crawler.utils.html_formatter import HtmlFormatter
from gen_crawler.configs.caam_config import CONF
from gen_crawler.logs.crawler_logger import spider_logger

class CaamNews(IndexSpider):

    name = "caam"
    _config = CONF

    def _get_result(self, response, config):
        rel = []
        conf = config
        results = response.xpath("//div[@class='xwzxlist xwzxlist_noline']/ul/li")
        if not results:
            spider_logger.error("Can't get url lists from %s" % conf['url'])
            return
        # 提取搜索结果
        for ul in results:
            item = Caam()
            # 从搜索结果页抽取信息
            item['crawl_url'] = "http://www.caam.org.cn"+ul.xpath("./a/@href").extract()[0]
            item['title'] = ul.xpath("./a/text()").extract()
            item['keyword'] = conf['keyword']
            publishtime = ul.xpath("./span/text()").extract()[0]
            try:
                item['publish_time'] = datetime.strptime(publishtime, "%Y-%m-%d %H:%M:%S")
            except Exception, e:
                spider_logger.info("Auto convert date format in %s" % item['crawl_url'])
                item['publish_time'] = datetime.strptime(publishtime+" 00:00:00", "%Y-%m-%d %H:%M:%S") 
            rel.append(item)
        return rel

    def _next_result_page(self, response):
        attr = re.split("-|.html", response.url)
        page = int(attr[-2])
        pages = response.xpath("//div[@class='the_pages']/div/a[last()]/@href").extract()[0]
        maxpage = int(re.split("-|.html", pages)[-2])
        crawlpage = 3
        if page < (maxpage if self.crawl_mode == 1 else(crawlpage if crawlpage<maxpage else maxpage)):
            page += 1
            attr[-2] = str(page)
        else:
            spider_logger.error("Can't get next page from %s" % response.url)
            return 
        return "-".join(attr[:-1])+".html"

    def _finish_item(self, item, response):
        # 继续提取信息
        item['crawl_website'] = u"中国汽车工业协会"
        item['atc'] = 0
        item['source_website'] = response.xpath("//div[@class='timecont']/ul/li[last()]/text()").extract()
        # content
        content = response.xpath("//div[@class='newstext']/p").extract()
        item['content'] = HtmlFormatter.format_content(content[0])
        # image
        item['image_urls'] = []
        for img_url in response.xpath("//div[@class='newstext']//img/@src").extract():
            if re.match("http.*", img_url):
                item['image_urls'].append(img_url)
        return item
