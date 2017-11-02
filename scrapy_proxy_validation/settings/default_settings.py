from scrapy_proxy_validation.downloadermiddlewares.proxy_validation import \
    Validation

SIGNALS = [Validation(exception='scrapy.exception_a',
                      signal='signal.signal_a',
                      signal_deferred='signal.signal_deferred_a'),
           Validation(exception='scrapy.exception_b',
                      signal='signal.signal_b',
                      signal_deferred='signal.signal_deferred_b',
                      limit=5)]

RECYCLE_REQUEST = 'scrapy_proxy_validation.utils.recycle_request.recycle_request'
