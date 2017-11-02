from unittest import TestCase

from scrapy.http import Request

from scrapy_proxy_validation.utils.recycle_request import recycle_request


class RecycleRequestTest(TestCase):
    def test_recycle_request(self):
        request = Request(url='http://www.httpbin.org',
                          meta={'proxy': 'http://localhost:8080'})

        r = recycle_request(request)

        self.assertTrue(r.dont_filter)
        self.assertNotIn('proxy', r.meta)
