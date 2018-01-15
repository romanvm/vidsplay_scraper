# coding: utf-8
# Created on: 15.01.2018
# Author: Roman Miroshnychenko aka Roman V.M. (roman1972@gmail.com)

from typing import Iterator
import scrapy

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

    def parse_video(self, response: scrapy.http.Response) -> dict:
        title = response.xpath(
            '/html/body/div[1]/div/div/div/div/main/article/div/header/h1/text()'
        ).extract_first()
        thumbnail = response.xpath(
            '/html/body/div[1]/div/div/div/div/main/article/div/div/div[2]/div[1]/meta[@itemprop="thumbnailUrl"]/@content'
        ).extract_first()
        url = response.xpath(
            '/html/body/div[1]/div/div/div/div/main/article/div/div/div[2]/div[1]/meta[@itemprop="contentURL"]/@content'
        ).extract_first()
        return {
            'category': response.meta['category'],
            'title': title,
            'thumbnail': thumbnail,
            'url': url
        }
