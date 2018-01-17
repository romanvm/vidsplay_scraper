# coding: utf-8
# Created on: 15.01.2018
# Author: Roman Miroshnychenko aka Roman V.M. (roman1972@gmail.com)

from typing import Iterator
import scrapy


class VideosSpider(scrapy.Spider):
    """Parse videos from vidsplay.com"""
    name = 'videos'
    start_url = 'https://www.vidsplay.com'

    def start_requests(self) -> Iterator[scrapy.Request]:
        """Entry point for our spider"""
        yield scrapy.Request(self.start_url, callback=self.parse)

    def parse(self, response: scrapy.http.Response) -> Iterator[scrapy.Request]:
        """Parse vidsplay.com index page"""
        category_urls = response.xpath(
            '/html/body/div[1]/div/div/div/aside/section[3]/div/ul/li/a/@href'
        ).extract()
        for url in category_urls[:3]:  # We want to be nice and scrap only 3 items
            yield response.follow(url, callback=self.parse_category)

    def parse_category(self, response: scrapy.http.Response) -> Iterator[scrapy.Request]:
        """Parse a video category page"""
        base_selector = response.xpath(
            '/html/body/div[1]/div/div/div/div/main/article'
        )
        category = base_selector.xpath(
            './header/h1/text()'
        ).extract_first()
        video_selectors = base_selector.xpath(
            './div/div[1]/div/div/div/div[@class="pt-cv-ifield"]'
        )
        for selector in video_selectors[:3]:  # We want to be nice and scrap only 3 items
            url = selector.xpath('./p/a/@href').extract_first()
            # ``meta`` argument can be used to pass data to downstream spider callbacks
            yield response.follow(url,
                                  callback=self.parse_video,
                                  meta={'category': category})

    def parse_video(self, response: scrapy.http.Response) -> Iterator[dict]:
        """Parse a video details page"""
        base_selector = response.xpath(
            '/html/body/div[1]/div/div/div/div/main/article/div'
        )
        title = base_selector.xpath(
            './header/h1/text()'
        ).extract_first()
        thumbnail = base_selector.xpath(
            './div/div[2]/div[1]/meta[@itemprop="thumbnailUrl"]/@content'
        ).extract_first()
        url = base_selector.xpath(
            './div/div[2]/div[1]/meta[@itemprop="contentURL"]/@content'
        ).extract_first()
        yield {
            'category': response.meta['category'],
            'title': title,
            'thumbnail': thumbnail,
            'url': url
        }
