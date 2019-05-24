import scrapy
import json

from ctt_hust.spiders.utils import compare_time
from datetime import date
today = date.today()

class HustSpider(scrapy.Spider):
    name = 'ctt_hust'
    start_urls = [
                    'https://ctt-daotao.hust.edu.vn/?page=' + str(v) +'&tabID=1' for v in range(1, 20)
                ]

    def __init__(self):
        self.cur_page = 0
        self.time_dic = {}
        self.processing_day = today.strftime('%d/%m/%Y')
        f = open('last_day.txt')
        self.last_day = f.read()
        f.close()

    def parse(self, response):
        if compare_time(self.processing_day, self.last_day):
            list_news = response.css('.assetContent')
            news_urls = []
            for v in list_news:
                url = v.css('a::attr(href)').get()
                time = v.css('i::text').get()
                news_urls.append([url, time])
            
            self.processing_day = time

            for url, time in news_urls:
                self.time_dic.update({url.split('/')[-1]: time})
                yield scrapy.Request(url='https://ctt-daotao.hust.edu.vn' + url, callback=self.parse_page)

    def parse_page(self, response):
        sentences = response.css('.l48contentRight span::text').getall()
        content = ' '.join(v for v in sentences)

        title = response.css('.l48RightMain h3::text').get()
        type_news_1 = response.css('.cap1 a::text').get().replace('\n', '')
        type_news_2 = response.css('.cap2 a::text').get()
        type_news_2 = ' '.join([x for x in type_news_2.split( ) if x != ''])

        if compare_time(self.time_dic[response.url.split('/')[-1]], self.last_day):
            with open('ctt_hust_4.json', 'a') as f:
                f.write(json.dumps({
                    'title': title,
                    'content': content.replace('\n', ''),
                    'url': response.url,
                    'type_lv1': type_news_1,
                    'type_lv2': type_news_2,
                    'time': self.time_dic[response.url.split('/')[-1]]
                }, ensure_ascii=False))
                f.write(',\n')
        
        with open('last_day.txt', 'w') as f:
            f.write(today.strftime('%d/%m/%Y'))
