__author__ = 'msahnov'
import re
import traceback
import feedparser
import logging

import requests
from bs4 import BeautifulSoup


from core.models import Pasty
from core.utils import remove_html_tags, to_date


logger = logging.getLogger(__name__)


def GetParser(source):
    """Kind of factory for parsers"""
    parsers = {
        'stishkipirozhki_ru': StishkiPirozhkiRssParser,
        'pirozhki_ru_livejournal_com': RssParser,
        'perashki_ru': PerashkiParser
    }
    parser_class = parsers.get(source.parser_key())
    if parser_class:
        return parser_class(source)
    else:
        raise NoSuchParserError(source.parser_key())


class StopParsing(Exception): pass


class NoSuchParserError(Exception): pass


class ParseError(Exception): pass


class BaseParser(object):

    MAX_LENGTH = 255

    def __init__(self, source):
        self.source = source
        self.parsed_entries = []
        self.raw_entries = []
        self.data = None
        self.last_update = None

    def parse(self):
        try:
            self.feed_data()
            self.check_last_update_date()
            self.parse_entries()
        except (StopParsing, NoSuchParserError):
            raise
        except Exception as error:
            raise ParseError(traceback.format_exc(), error)

    def feed_data(self):
        raise NotImplementedError

    def parse_entry(self, entry):
        raise NotImplementedError

    def check_last_update_date(self):
        if self.source.sync_date and \
                        self.source.sync_date >= self.last_update:
            raise StopParsing("Source is already up to date")

    def parse_entries(self):
        for entry in self.raw_entries:
            self.parsed_entries.append(
                self.parse_entry(entry)
            )
            self.parsed_entries = filter(None, self.parsed_entries)

    def save(self):
        for entry in self.parsed_entries:
            if self.source.sync_date and \
                            entry.date <= self.source.sync_date:
                continue
            entry.save()


class RssParser(BaseParser):

    def feed_data(self):
        self.data = feedparser.parse(self.source.sync_url)
        self.raw_entries = self.data.entries
        self.last_update = to_date(self.data.feed.updated_parsed)

    def process_text(self, text):
        """Some rss pastries specific text processing"""
        space_pattern = re.compile('\s\s+')
        text = remove_html_tags(text)
        text = space_pattern.sub(' ', text)
        return text

    def parse_entry(self, entry):
        text = self.process_text(entry['summary_detail']['value'])
        if len(text) > self.MAX_LENGTH or \
                not remove_html_tags(text):
            return None
        pasty = Pasty()
        pasty.text = text
        pasty.date = to_date(entry['published_parsed']) or self.last_update
        pasty.published = True
        pasty.source = self.source.url
        return pasty


class StishkiPirozhkiRssParser(RssParser):

    def feed_data(self):
        self.data = feedparser.parse(self.source.sync_url)
        self.raw_entries = self.data.entries
        # stishkipiroshki has no updated_parsed in feed info, so I will find update time in such strange way
        self.last_update = to_date(
            max(
                [e.published_parsed for e in self.raw_entries]
            ))


class PerashkiParser(BaseParser):

    def feed_data(self):
        self.data = BeautifulSoup(requests.get(self.source.sync_url).content).find_all(
            class_='TextContainer'
        )
        self.raw_entries = self.data
        self.last_update = to_date(self.data[0].find(class_='date').text)

    def parse_entry(self, entry):
        text = entry.find(class_='Text').text.replace('\r\n', '<br/>')
        if len(text) > self.MAX_LENGTH:
            return None
        pasty = Pasty()
        pasty.text = text
        pasty.date = to_date(entry.find(class_='date').text)
        pasty.published = True
        pasty.source = self.source.url
        return pasty
