# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/data/items.html

import scrapy


class Base(scrapy.Item):
    """需抽取的基本信息
    """

    # 主键：数据库自动生成
    id = scrapy.Field()
    # 必须属性
    crawl_url = scrapy.Field()
    title = scrapy.Field()
    crawl_website = scrapy.Field()
    publish_time = scrapy.Field()  # 发布时间：datatime类型
    content = scrapy.Field()
    stock = scrapy.Field()  # 外键：stock表的主键值，通过字典self.queries可取到
    # 非必要属性
    digest = scrapy.Field()  # 爬取时可不填写


class Auto360(Base):
    """auto360网站通用爬虫
    """

    # 可选属性
    author = scrapy.Field()  # 列表：本新闻的记者、编辑等
    source_website = scrapy.Field()
    source_url = scrapy.Field()
    keyword = scrapy.Field()  # 列表：本新闻的关键字
    maxpages = scrapy.Field()  #列表页最大页数
    # 图片相关
    image_path = scrapy.Field()
    image_urls = scrapy.Field()  # 列表：本新闻相关的图片链接
    images = scrapy.Field()  # 图片列表，每张图片包含path和url属性
    atc = scrapy.Field()  #是否有附件
    atc_name = scrapy.Field()  #附件名字
    atc_format = scrapy.Field()  #附件格式
    atc_url = scrapy.Field()  #附件链接
    atc_path = scrapy.Field()  #附件本地路径

class Caam(Base):
    """caam网站通用爬虫
    """

    # 可选属性
    author = scrapy.Field()  # 列表：本新闻的记者、编辑等
    source_website = scrapy.Field()
    source_url = scrapy.Field()
    keyword = scrapy.Field()  # 列表：本新闻的关键字
    maxpages = scrapy.Field()  #列表页最大页数
    # 图片相关
    image_path = scrapy.Field()
    image_urls = scrapy.Field()  # 列表：本新闻相关的图片链接
    images = scrapy.Field()  # 图片列表，每张图片包含path和url属性
    atc = scrapy.Field()  #是否有附件
    atc_name = scrapy.Field()  #附件名字
    atc_format = scrapy.Field()  #附件格式
    atc_url = scrapy.Field()  #附件链接
    atc_path = scrapy.Field()  #附件本地路径

class Autohome(Base):
    """autohome网站通用爬虫
    """

    # 可选属性
    author = scrapy.Field()  # 列表：本新闻的记者、编辑等
    source_website = scrapy.Field()
    source_url = scrapy.Field()
    keyword = scrapy.Field()  # 列表：本新闻的关键字
    maxpages = scrapy.Field()  #列表页最大页数
    # 图片相关
    icon = scrapy.Field()
    image_path = scrapy.Field()
    image_urls = scrapy.Field()  # 列表：本新闻相关的图片链接
    images = scrapy.Field()  # 图片列表，每张图片包含path和url属性
    atc = scrapy.Field()  #是否有附件
    atc_name = scrapy.Field()  #附件名字
    atc_format = scrapy.Field()  #附件格式
    atc_url = scrapy.Field()  #附件链接
    atc_path = scrapy.Field()  #附件本地路径

class Chinaev(Base):
    """autohome网站通用爬虫
    """

    # 可选属性
    author = scrapy.Field()  # 列表：本新闻的记者、编辑等
    source_website = scrapy.Field()
    source_url = scrapy.Field()
    keyword = scrapy.Field()  # 列表：本新闻的关键字
    maxpages = scrapy.Field()  #列表页最大页数
    # 图片相关
    icon = scrapy.Field()
    image_path = scrapy.Field()
    image_urls = scrapy.Field()  # 列表：本新闻相关的图片链接
    images = scrapy.Field()  # 图片列表，每张图片包含path和url属性
    atc = scrapy.Field()  #是否有附件
    atc_name = scrapy.Field()  #附件名字
    atc_format = scrapy.Field()  #附件格式
    atc_url = scrapy.Field()  #附件链接
    atc_path = scrapy.Field()  #附件本地路径

class Cpca1(Base):
    """autohome网站通用爬虫
    """

    # 可选属性
    author = scrapy.Field()  # 列表：本新闻的记者、编辑等
    source_website = scrapy.Field()
    source_url = scrapy.Field()
    keyword = scrapy.Field()  # 列表：本新闻的关键字
    maxpages = scrapy.Field()  #列表页最大页数
    # 图片相关
    icon = scrapy.Field()
    image_path = scrapy.Field()
    image_urls = scrapy.Field()  # 列表：本新闻相关的图片链接
    images = scrapy.Field()  # 图片列表，每张图片包含path和url属性
    atc = scrapy.Field()  #是否有附件
    atc_name = scrapy.Field()  #附件名字
    atc_format = scrapy.Field()  #附件格式
    atc_url = scrapy.Field()  #附件链接
    atc_path = scrapy.Field()  #附件本地路径