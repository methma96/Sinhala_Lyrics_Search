# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class LyricsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    artist = scrapy.Field()
    genre = scrapy.Field()
    lyricist = scrapy.Field()
    music_by = scrapy.Field()
    views = scrapy.Field()
    shares = scrapy.Field()
    lyric = scrapy.Field()
