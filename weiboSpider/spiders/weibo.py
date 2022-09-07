import scrapy
from scrapy import Request, FormRequest

import redis
import random
import js2xml
from cookies import COOKIES
from weiboSpider.items import *


class WeiboSpider(scrapy.Spider):
    name = 'weibo'
    allowed_domains = ['weibo.cn']
    start_urls = []
    _cookies = COOKIES

    ul_path = "user_list.txt"
    user_url = "https://m.weibo.cn/api/container/getIndex?containerid=100505{}"
    user_url_addition = "https://m.weibo.cn/api/container/getIndex?containerid=230283{}_-_INFO"
    weibo_url = "https://weibo.cn/u/{}"
    weibo_detail_url = "https://m.weibo.cn/detail/{}"
    comment_url = "https://m.weibo.cn/api/comments/show"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cache = redis.StrictRedis(host='localhost', port=6379)
        self.start_urls = self.get_start_urls()

        # 将已爬取的结果导入redis
        # self.connection = sqlite3.connect(self.settings.SQLITE_PATH)
        # cursor = self.connection.cursor()
        # rows = cursor.execute("SELECT weibo_id FROM WEIBO")
        # for row in rows:
        #     self.cache.sadd('weibo_id', row[0])

    def get_start_urls(self):
        if self.cache.exists('user_id'):
            self.init_parser = self.parse_weibo
            user_set = self.cache.smembers('user_id')
            return [self.weibo_url.format(uid.decode()) for uid in user_set]
        elif self.ul_path:
            self.init_parser = self.parse_user
            with open(self.ul_path, "r") as f:
                return [self.user_url.format(line) for line in f]
        return []

    @property
    def cookies(self):
        return random.choice(self._cookies)

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url, callback=self.init_parser, cookies=self.cookies)

    def parse_user(self, response):
        datapack = response.json()
        if datapack["ok"]:
            data = datapack.get("data")
            userInfo = data.get("userInfo")
            user = UserItem()
            user["user_id"] = userInfo.get("id")                        # 用户id
            user["screen_name"] = userInfo.get("screen_name")           # 昵称
            user["statuses_count"] = userInfo.get("statuses_count")     # 微博数
            user["verified"] = userInfo.get("verified")                 # 是否认证
            user["verified_type"] = userInfo.get("verified_type")       # 认证类型
            user["verified_reason"] = userInfo.get("verified_reason")   # 认证信息
            user["description"] = userInfo.get("description")           # 简介
            user["gender"] = userInfo.get("gender")                     # 性别
            user["urank"] = userInfo.get("urank")                       # 微博等级
            user["mbrank"] = userInfo.get("mbrank")                     # 微博会员等级
            user["follow_count"] = userInfo.get("follow_count")         # 关注数
            user["followers_count"] = userInfo.get("followers_count")   # 粉丝数

            url = self.user_url_addition.format(user["user_id"])
            yield Request(url, callback=self.parse_user_addition, cookies=self.cookies, meta={"item": user}, dont_filter=True)
        else:
            yield Request(response.url, callback=self.parse_user, dont_filter=True)

    def parse_user_addition(self, response):
        datapack = response.json()
        if datapack["ok"]:
            data = datapack.get("data")
            cards = sum([card["card_group"] for card in data["cards"]], [])
            userDict = {card.get("item_name"): card.get(
                "item_content") for card in cards}

            user = response.meta["item"]
            user["created_at"] = userDict.get("注册时间")               # 注册时间
            user["sunshine"] = userDict.get("阳光信用")                 # 阳光信用
            user["birthday"] = userDict.get("生日")                     # 生日
            user["location"] = userDict.get("所在地")                   # 所在地
            user["education"] = userDict.get("大学")                    # 教育经历
            user["company"] = userDict.get("公司")                      # 公司信息
            yield user

            url = self.weibo_url.format(user["user_id"])
            yield Request(url, callback=self.parse_weibo, cookies=self.cookies)

    def parse_weibo(self, response):
        wid_list = response.css("div.c[id]::attr(id)").getall()
        for wid in wid_list:
            weibo_id = wid.lstrip("M_")
            if not self.cache.sismember('weibo_id', weibo_id):
                url = self.weibo_detail_url.format(weibo_id)
                yield Request(url, callback=self.parse_weibo_detail)

        next = response.css("div.pa a::attr(href)").get()
        if next is not None:
            yield response.follow(next, callback=self.parse_weibo)

    def parse_weibo_detail(self, response):
        try:
            text = response.css("script::text").getall()
            xml = js2xml.parse(text[1])
            status = xml.cssselect("property[name='status']")[0]
            data = js2xml.jsonlike.make_dict(status)[1]
        except IndexError:
            yield Request(response.url, callback=self.parse_weibo_detail)
        else:
            weibo = WeiboItem()
            weibo_id = data.get("id")

            weibo["user_id"] = data["user"]["id"]
            weibo["weibo_id"] = weibo_id
            weibo["text"] = data.get("text")
            if data.get("pics"):
                pics = data["pics"]
                weibo["img"] = ','.join(pic["large"]["url"] for pic in pics)
            # weibo["video"] = info.get("pics")
            # weibo["locate"] =
            weibo["created_at"] = data.get("created_at")
            weibo["tool"] = data.get("source")
            weibo["reposts"] = data.get("reposts_count")
            weibo["comments"] = data.get("comments_count")
            weibo["attitudes"] = data.get("attitudes_count")
            weibo["original"] = True

            retweet = data.get("retweeted_status")
            if retweet:
                weibo["original"] = False
                user = retweet.get("user")
                if not user:
                    return
                weibo["ouid"] = user.get("id")
                weibo["owid"] = retweet.get("id")
                if retweet.get("isLongText"):
                    weibo["otext"] = retweet.get("longText", {}).get("longTextContent")
                else:
                    weibo["otext"] = retweet.get("text")
                if retweet.get("pics"):
                    weibo["oimg"] = '.'.join(pic["large"]["url"] for pic in retweet.get("pics"))
                # weibo["ovideo"] =
                weibo["odate"] = retweet.get("created_at")
                weibo["otool"] = retweet.get("source")
                weibo["oreposts"] = retweet.get("reposts_count")
                weibo["ocomments"] = retweet.get("comments_count")
                weibo["oattitudes"] = retweet.get("attitudes_count")

            self.cache.sadd('weibo_id', weibo_id)
            yield weibo

            if weibo["comments"] > 0:
                formdata = {"id": weibo["weibo_id"],
                            "page": "1"}
                yield FormRequest(self.comment_url, callback=self.parse_comment, method="GET", cookies=self.cookies, formdata=formdata, meta={"formdata": formdata})

    def parse_comment(self, response):
        formdata = response.meta["formdata"]
        datapack = response.json()
        if datapack["ok"]:
            data = datapack["data"]
            weibo_id = formdata["id"]
            page = int(formdata["page"])
            for comment in data["data"]:
                item = CommentItem()
                item["weibo_id"] = weibo_id
                item["comment_id"] = comment["id"]
                item["created_at"] = comment["created_at"]
                item["text"] = comment["text"]
                item["user_id"] = comment["user"]["id"]
                item["screen_name"] = comment["user"]["screen_name"]
                if comment.get("pic"):
                    item["pic"] = comment["pic"]["large"]["url"]
                item["like_count"] = comment["like_counts"]
                yield item

            if page < data["max"]:
                formdata["page"] = str(page + 1)
                yield FormRequest(self.comment_url, callback=self.parse_comment, method="GET", cookies=self.cookies, formdata=formdata, meta={"formdata": formdata})
        else:
            yield FormRequest(self.comment_url, callback=self.parse_comment, method="GET", cookies=self.cookies, formdata=formdata)
