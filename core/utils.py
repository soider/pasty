# -*- coding: utf-8 -*-
import datetime
import time

from bs4 import BeautifulSoup


def remove_html_tags(html):
    """Remove each tag from :html:"""
    return BeautifulSoup(html).getText()


def to_date(date_object):
    """Try to convert :date_object: to :datetime:"""
    if isinstance(basestring, date_object):
        return datetime.datetime.strptime(
            date_object,
            '%d.%m.%Y'
        )
    if not date_object:
        return None
    return datetime.datetime.fromtimestamp(time.mktime(date_object))