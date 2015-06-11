# -*- coding: utf-8 -*-
import logging
import datetime


from core.parsing import GetParser, StopParsing, NoSuchParserError, ParseError


logger = logging.getLogger(__name__)


class SyncError(Exception): pass


def sync_rss_source(source):
    try:
        parser = GetParser(source)
        parser.parse()
        parser.save()
        source.sync_date = datetime.datetime.now()
        source.save()
    except StopParsing as reason:
        logger.warning("Skip %s in case of %s", source.title, reason.message)
    except NoSuchParserError:
        logger.warning("No parser for %s", source.parser_key())
        return
    except ParseError as error:
        logger.error("Sync process for %s failed",
                     source.title,
                     exc_info=1)
        raise SyncError(error)