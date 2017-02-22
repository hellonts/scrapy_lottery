#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Author: ylf
#
# Created: 16-12-19

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LotteryItem(scrapy.Item):
    issue = scrapy.Field()
    opencode   = scrapy.Field()
    opentime   = scrapy.Field()
    tablename   = scrapy.Field()


class LotteryBackupItem(scrapy.Item):
    issue = scrapy.Field()
    opencode   = scrapy.Field()
    opentime   = scrapy.Field()
    tablename   = scrapy.Field()

