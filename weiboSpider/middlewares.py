# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import base64
from urllib.request import Request
from scrapy import FormRequest, signals

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter
from scrapy.downloadermiddlewares.retry import RetryMiddleware
from twisted.internet.error import TCPTimedOutError, TimeoutError


class WeibospiderSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class WeibospiderDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called

        # if "detail" in request.url:
        # if "container" in request.url:
        #     return
        # proxy_user_pass = b"ZFE41725212947551145:ia9k6etXHoC4"
        # encoded_user_pass = base64.encodebytes(proxy_user_pass)

        # request.headers["Proxy-Authorization"] = b"Basic " + encoded_user_pass
        # request.meta["proxy"] = "http://dyn.horocn.com:50000"
        # request.headers["Proxy-Authorization"] = b"Basic WkZFNDE3MjUyMTI5NDc1NTExNDU6aWE5azZldFhIb0M0\n"
        # request.headers["Proxy-Connection"] = "close"
        # request.headers["Connection"] = "close"
        # request.dont_filter = True
        # elif not request.meta.get("proxy"):
        #     request.meta["proxy"] = get_proxy()
        # if not request.meta.get("proxy"):
        #     request.meta["proxy"] = get_proxy()
        return

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.
        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        # if response.status == 403:
        #     if "max_id" in request.url:
        #         request.url = request.url.split("max_id")[0]
        #     proxy = request.meta["proxy"]
        #     request.meta["proxy"] = get_proxy()
        #     proxy_pool.add(proxy)
        #     return request

        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


# class ProxyRetryMiddleware(RetryMiddleware):
#     def process_exception(self, request, exception, spider):
#         if isinstance(
#                 exception, TimeoutError) or isinstance(
#                 exception, TCPTimedOutError) or isinstance(
#                 exception, ConnectionRefusedError):
#             return request
