# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapyNormalItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # text = Scrapy.Field()
    # text = Scrapy.Field()
    # text = Scrapy.Field()

    def get_insert_sql(self):
        insert_sql="""
        insert into tablename(Field_name1,Field_name2,Field_name3,Field_name4,Field_name5,Field_name6)
        VALUES (%s,%s,%s,%s,%s,%s)
        
        """
        params=(
            self['Field_name1'], self['Field_name2'], self['Field_name3'], self['Field_name4'],
            self['Field_name5'], self['Field_name6']
        )
        return insert_sql,params

