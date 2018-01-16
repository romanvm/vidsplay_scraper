# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from openpyxl import Workbook
from openpyxl.styles import Font
from .settings import OUT_FILE


class XlsxPipeline(object):
    """Save scraped data to an XLSX spreadsheet"""

    def open_spider(self, spider):
        """Start scraping"""
        # Create an Excel workbook
        self._wb = Workbook()
        # Select the active spreadsheet
        self._ws = self._wb.active
        self._ws.title = 'Videos'
        self._ws.append(['Category', 'Title', 'Thumbnail', 'Video URL'])
        row = list(self._ws.rows)[0]
        for cell in row:
            cell.font = Font(bold=True)

    def process_item(self, item, spider):
        # Append a row to the spreadsheet
        self._ws.append([
            item['category'],
            item['title'],
            item['thumbnail'],
            item['url']
        ])
        return item

    def close_spider(self, spider):
        """Stop scraping"""
        # Save the Excel workbook
        self._wb.save(OUT_FILE + '.xlsx')
