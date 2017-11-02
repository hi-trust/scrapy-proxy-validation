import pprint

from scrapy.http import Request
from scrapy.spiders import Spider
from scrapy.utils.test import get_crawler
from twisted.internet.defer import inlineCallbacks
from twisted.internet.error import ConnectionClosed
from twisted.internet.error import ConnectionRefusedError
from twisted.trial.unittest import TestCase

from scrapy_proxy_validation.downloadermiddlewares.proxy_validation import \
    ProxyValidation
from scrapy_proxy_validation.downloadermiddlewares.proxy_validation import \
    Validation

pp = pprint.PrettyPrinter(indent=4)


class ProxyValidationTest(TestCase):
    settings = {
        'SIGNALS': [
            Validation(
                exception='twisted.internet.error.ConnectionRefusedError',
                signal='scrapy.signals.spider_closed'),
            Validation(
                exception='twisted.internet.error.ConnectionLost',
                signal='scrapy.signals.spider_closed',
                signal_deferred='scrapy.signals.spider_closed',
                limit=5)],
        'RECYCLE_REQUEST': 'scrapy_proxy_validation.utils.recycle_request.recycle_request'
    }

    def get_spider_and_mw(self):
        crawler = get_crawler(Spider, settings_dict=self.settings)
        spider = crawler._create_spider('foo')
        return spider, ProxyValidation.from_crawler(crawler)

    @inlineCallbacks
    def test_process_exception_with_validated_exception(self):
        spider, mw = self.get_spider_and_mw()

        request = Request(url='http://www.httpbin.org',
                          meta={'proxy': 'http://localhost:8080'})

        result = yield mw.process_exception(
            request=request,
            exception=ConnectionRefusedError,
            spider=spider)

        _request = request.replace(dont_filter=True)
        _request.meta.pop('proxy')

        self.assertDictEqual(
            _request.__dict__,
            result.__dict__)

    @inlineCallbacks
    def test_process_exception_with_invalidated_exception(self):
        spider, mw = self.get_spider_and_mw()

        request = Request(url='http://www.httpbin.org',
                          meta={'proxy': 'http://localhost:8080'})

        result = yield mw.process_exception(
            request=request,
            exception=ConnectionClosed,
            spider=spider)

        self.assertIsNone(result)
