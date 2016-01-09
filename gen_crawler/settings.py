# -*- coding: utf-8

# Scrapy settings for general-crawler project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'general_crawler'
SPIDER_MODULES = ['gen_crawler.spiders']


DATA_BASE = "/home/plustock/data/crawler"

# 下载器中间件
DOWNLOADER_MIDDLEWARES = {
    'gen_crawler.middlewares.random_useragent.RandomUserAgent': 100,
    }

# 持久化组件
ITEM_PIPELINES = {
    'gen_crawler.pipelines.duplicate_removal.DuplicateRemoval': 100,
    'gen_crawler.pipelines.image_pipelines.ArticleImagesPipeline': 300,
    'gen_crawler.pipelines.auto360_pipelines.Auto360Pipeline': 500,
    'gen_crawler.pipelines.caam_pipelines.CaamPipeline': 510,
    'gen_crawler.pipelines.autohome_pipelines.AutohomePipeline': 520,
    'gen_crawler.pipelines.chinaev_pipelines.ChinaevPipeline': 530,
    'gen_crawler.pipelines.cpca1_pipelines.Cpca1Pipeline': 540,

    }

# 图片
IMAGES_EXPIRES = 10
IMAGES_STORE = DATA_BASE+"/images/general-crawler"

# 日志
LOG_DIR = DATA_BASE+"/logs"

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'passwd': '1qaz2wsx',
    'db': 'goblin',
    'charset': 'utf8'
    }

