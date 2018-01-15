# coding: utf-8
# Created on: 15.01.2018
# Author: Roman Miroshnychenko aka Roman V.M. (roman1972@gmail.com)

from typing import Iterator
import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst
from vidsplay_scraper.items import VideoItem

HOME_URL = 'https://www.vidsplay.com'


class VideosSpider(scrapy.Spider):
    name = 'videos'

    def start_requests(self):
        yield scrapy.Request(HOME_URL, callback=self.parse)

    def parse(self, response: scrapy.http.Response) -> Iterator[scrapy.Request]:
        category_urls = response.xpath(
            '/html/body/div[1]/div/div/div/aside/section[3]/div/ul/li/a/@href'
        ).extract()
        for url in category_urls:
            yield scrapy.Request(url, callback=self.parse_category)

    def parse_category(self, response: scrapy.http.Response) -> Iterator[scrapy.Request]:
        category = response.xpath(
            '/html/body/div[1]/div/div/div/div/main/article/header/h1/text()'
        ).extract_first()
        video_selectors = response.xpath(
            '/html/body/div[1]/div/div/div/div/main/article/div/div[1]/div/div/div/div[@class="pt-cv-ifield"]'
        )
        for selector in video_selectors:
            url = selector.xpath('//p/a/@href').extract_first()
            yield scrapy.Request(url,
                                 callback=self.parse_video,
                                 meta={'category': category})

    def parse_video(self, response: scrapy.http.Response) -> scrapy.Item:
        loader = ItemLoader(item=VideoItem(), response=response)
        loader.default_output_processor = TakeFirst()
        loader.add_value('category', response.meta['category'])
        loader.add_xpath(
            'title',
            '/html/body/div[1]/div/div/div/div/main/article/div/header/h1/text()'
        )
        loader.add_xpath(
            'thumbnail',
            '/html/body/div[1]/div/div/div/div/main/article/div/div/div[2]/div[1]/meta[@itemprop="thumbnailUrl"]/@content'
        )
        loader.add_xpath(
            'url',
            '/html/body/div[1]/div/div/div/div/main/article/div/div/div[2]/div[1]/meta[@itemprop="contentURL"]/@content'
        )
        return loader.load_item()
