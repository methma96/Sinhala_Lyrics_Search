import scrapy
from lyrics.items import LyricsItem
from datetime import datetime
import re
from mtranslate import translate
import pickle



translated_dict = {}           


def translate(string):
    
    if string in translated_dict:
        return translated_dict[string]
    elif string.lower() == "unknown":
        return ''
    else:
        translated = translate(string, 'si', 'en')
        translated_dict[string] = translated
        return translated


def translate_array(stringList):
    temp = []
    for string in stringList:
        temp.append(translate(string))
    return temp


class LyricsSpider(scrapy.Spider):
    name = "lyrics"
    start_urls = ['https://sinhalasongbook.com/all-sinhala-song-lyrics-and-chords/?_page=' + str(i) for i in range(1,10)]            # max range(1, 23)

    def parse(self, response):
        global translated_dict

        try:
            translated_dict = pickle.load(open('../translated_dict.pickle', 'rb'))
        except (OSError, IOError):
            pickle.dump(translated_dict, open('../translated_dict.pickle', 'wb'))

        for href in response.xpath("//main[contains(@id, 'genesis-content')]//div[contains(@class, 'entry-content')]//div[contains(@class, 'pt-cv-wrapper')]//h4[contains(@class, 'pt-cv-title')]/a/@href"):
            url = href.extract()

            yield scrapy.Request(url, callback=self.parse_dir_contents)
    

    def parse_dir_contents(self, response):
        global translated_dict

        item = LyricsItem()

       

        # song name
        temp = response.xpath("//div[contains(@class, 'site-inner')]//header[contains(@class, 'entry-header')]/h1/text()").extract()[0]
        temp = re.split('\||–|-', temp)
        item['title'] = temp[1].strip()

        # artist name
        temp = response.xpath("//div[contains(@class, 'entry-content')]//div[contains(@class, 'su-column su-column-size-3-6')]//span[contains(@class, 'entry-categories')]/a/text()").extract()
        if len(temp) == 0:
            item['artist'] = []
        else:
            temp = translate_array(temp)
            item['artist'] = temp
        
        # genre
        temp = response.xpath("//div[contains(@class, 'entry-content')]//div[contains(@class, 'su-column su-column-size-3-6')]//span[contains(@class, 'entry-tags')]/a/text()").extract()
        if len(temp) == 0:
            item['genre'] = []
        else:
            temp = translate_array(temp)
            item['genre'] = temp
        
        # lyric writer
        temp = response.xpath("//div[contains(@class, 'entry-content')]//div[contains(@class, 'su-column su-column-size-2-6')]//span[contains(@class, 'lyrics')]/a/text()").extract()
        if len(temp) == 0:
            item['lyricist'] = []
        else:
            temp = translate_array(temp)
            item['lyricist'] = temp

        # music director
        temp = response.xpath("//div[contains(@class, 'entry-content')]//div[contains(@class, 'su-column su-column-size-2-6')]//span[contains(@class, 'music')]/a/text()").extract()
        if len(temp) == 0:
            item['music_by'] = []
        else:
            temp = translate_array(temp)
            item['music_by'] = temp


        # no of views
        try:
            temp = response.xpath("//div[contains(@class, 'entry-content')]/div[contains(@class, 'tptn_counter')]/text()").extract()[0]
            temp = int(re.sub('[^0-9,]', "", temp).replace(',', ''))
            item['views'] = temp
        except:
            item['views'] = None

        # no of shares
        try:
            temp = response.xpath("//div[contains(@class, 'entry-content')]//div[contains(@class, 'nc_tweetContainer swp_share_button total_shares total_sharesalt')]/span[contains(@class, 'swp_count')]/text()").extract()[0]
            temp = int(re.sub('[^0-9,]', "", temp).replace(',', ''))
            item['shares'] = temp
        except:
            item['shares'] = None

        # lyric
        temp = response.xpath("//div[contains(@class, 'entry-content')]//pre/text()").extract()
        lyrics = ''
        line_1 = True
        line_2 = False

        for line in temp:
            line_content = (re.sub("[\da-zA-Z\-—\[\]\t\@\_\!\#\+\$\%\^\&\*\(\)\<\>\?\|\}\{\~\:\∆\/]", "", line)).split('\n')
            
            for lline in line_content:
                if lline == '' or lline.isspace():
                    if not line_2:
                        line_2 = True
                        lyrics += '\n'
                else:
                    line_1  = False
                    line_2 = False
                    lyrics += lline.strip()
            
            if not line_1 :
                line_1  = True
                lyrics += '\n'

        item['lyric'] = lyrics

        pickle.dump(translated_dict, open('../translated_dict.pickle', 'wb'))

        yield item
