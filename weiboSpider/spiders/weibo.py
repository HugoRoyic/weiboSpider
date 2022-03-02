import scrapy
from scrapy.http import FormRequest

import json
import random
import js2xml
from tools import weibo_id_convert
from weiboSpider.items import *


class WeiboSpider(scrapy.Spider):
    name = 'weibo'
    allowed_domains = ['weibo.cn']
    start_urls = []
    cookies = [
        {
            'SCF': 'AldouH3y5yKdY4H_8j5SPIE9IyMy7fn6TuSVLr23K7T7gXMvbI8Ucw3YuDay-D6U7fbOUtinn1SVcxTlxgWbR4g.',
            'SUB': '_2A25M4uhuDeRhGeNH7FsT-CvLyDqIHXVsLIgmrDV6PUJbktCOLW78kW1NSmk7doLGbL5aRpws-dfYx5cZQUh8w58m',
            'SUBP': '0033WrSXqPxfM725Ws9jqgMF55529P9D9WhvoqgYh-uOP7__crHo.RbU5NHD95Qf1KM4eonfS0ecWs4Dqcjmi--Xi-zRiK.ci--NiK.fiKyhi--4iKLFi-zci--ci-zfiKnpi--fi-2Xi-2Ni--fi-82i-2cdc9JIgSDqg7t',
            'SSOLoginState': '1642502207', '_T_WM': 'daee613bcfa6b4ac128d115ad5a2a1e4'},
        {
            "_T_WM": "bd4eced8c9026e0e21315ae06722d235",
            "SUB": "_2A25PFnDpDeRhGeFJ71EQ9yjFyTyIHXVs-RChrDV6PUJbktCOLWL7kW1Nf_qZmxcjlFLQe-OgA7kfgXHfCUkK0j-e",
            "SUBP":
            "0033WrSXqPxfM725Ws9jqgMF55529P9D9W5iWa3W4a_nSBhRuJbYDHAW5NHD95QNS0B0eKMc1Kz7Ws4DqcjMi--NiK.Xi-2Ri--ciKnRi-zNSKeXSozceK.0e5tt",
            "SSOLoginState": "1645347001"},
        {
            "loginScene": "102003",
            "SUB": "_2A25PFY5SDeRhGeFO6loR9SrNyjSIHXVs-RIarDV6PUJbkdCOLW7bkW1NQZDjOn1PdDWcWg6lEngt26CupLjhPage",
            "_T_WM": "86576543976",
            "MLOGIN": "1",
            "M_WEIBOCN_PARAMS": 'lfid%3D102803%26luicode%3D20000174'},
        {
            "loginScene": "102003",
            "SUB": "_2A25PFmZyDeRhGeBO6FIX8C3EyjiIHXVs-Qo6rDV6PUJbkdAKLWTnkW1NSg48L5u0XlweXj_hbmgCDpDLtUHNJkFW",
            "_T_WM": "40506336635",
            "MLOGIN": "1",
            "M_WEIBOCN_PARAMS": "lfid%3D102803%26luicode%3D20000174"},
        {
            "SUBP": "0033WrSXqPxfM725Ws9jqgMF55529P9D9WW7pHolrIlj3C7o3WVAq70N5NHD95Qce0ecehefSKBpWs4DqcjiBrHAwrSQdcSu",
            "ALF": "1647943972",
            "SUB": "_2A25PFmQnDeRhGeBN6FQR8yvJzz2IHXVs-QxvrDV6PUJbktB-LRX-kW1NRGq-o4AuySEW0WIAwogC7NqqRV-u7XW9",
            "SSOLoginState": "1645352055",
            "_T_WM": "87587616880",
            "WEIBOCN_FROM": "1110006030",
            "MLOGIN": "1",
            "M_WEIBOCN_PARAMS": "luicode%3D20000174%26uicode%3D20000174"},
        {
            "SUB": "_2A25PFmWMDeRhGeBN7FcX8C3Kyj-IHXVsYtBErDV8PUNbmtANLVH8kW9NRDkkV12gfSETOW_EO4PPIjcSweLu-nEW",
            "SUBP": "0033WrSXqPxfM725Ws9jqgMF55529P9D9WFZkzWyE-PoqTJlKZr_vk9Z5JpX5KMhUgL.Foq0S0-ceheceKe2dJLoIEjLxKMLBK-L1--LxKBLBonL1h5LxKqLBK5LBoMLxKML1-2L1hxJdNiXUg4L",
            "ULV": "1642470630439:9:1:1:736933640634.3807.1642470630430:1639613038828",
            "ALF": "1676888411",
            "SCF": "Alc2v0IUP-ljqe5Ynhb35YNcl-T5AzM_JEoIhGh9O4M6f_yIRTC7I6rB0zB4-UHbmuLATi9RJhhHCX3C63-aBGw.",
            "SSOLoginState": "1645352412",

        }]

    ul_path = "user_list.txt"
    user_url = "https://m.weibo.cn/api/container/getIndex?containerid=100505{}"
    user_url_addition = "https://m.weibo.cn/api/container/getIndex?containerid=230283{}_-_INFO"
    weibo_url = "https://weibo.cn/u/{}"
    weibo_detail_url = "https://m.weibo.cn/detail/{}"
    comment_url = "https://m.weibo.cn/api/comments/show"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.ul_path:
            with open(self.ul_path, "r") as f:
                for line in f:
                    self.start_urls.append(self.user_url.format(line))

    def random_cookies(self):
        return random.choice(self.cookies)

    def start_requests(self):
        for url in self.start_urls:
            yield FormRequest(url, callback=self.parse_user, method="GET", cookies=self.cookies)

    def parse_user(self, response):
        datapack = json.loads(response.body)
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
            yield FormRequest(url, callback=self.parse_user_addition, method="GET", cookies=self.random_cookies(), meta={"item": user}, dont_filter=True)
        else:
            yield FormRequest(response.url, callback=self.parse_user, method="GET", dont_filter=True)

    def parse_user_addition(self, response):
        datapack = json.loads(response.body)
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
            yield FormRequest(url, callback=self.parse_weibo, method="GET", cookies=self.random_cookies())

    def parse_weibo(self, response):
        wid_list = response.css("div.c[id]::attr(id)").getall()
        for wid in wid_list:
            url = self.weibo_detail_url.format(wid.lstrip("M_"))
            yield FormRequest(url, callback=self.parse_weibo_detail, method="GET")

        next = response.css("div.pa a::attr(href)").get()
        yield response.follow(next, callback=self.parse_weibo)

    def parse_weibo_detail(self, response):
        try:
            text = response.css("script::text").getall()
            xml = js2xml.parse(text[1])
            status = xml.cssselect("property[name='status']")[0]
            data = js2xml.jsonlike.make_dict(status)[1]
        except IndexError:
            yield FormRequest(response.url, callback=self.parse_weibo_detail, method="GET")
            return
        weibo = WeiboItem()

        weibo["user_id"] = data["user"]["id"]
        weibo["weibo_id"] = data.get("id")
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

        yield weibo

        if weibo["comments"] > 0:
            # formdata = {"id": weibo["weibo_id"],
            #             "mid": weibo["weibo_id"],
            #             "max_id_type": "0"}
            formdata = {"id": weibo["weibo_id"],
                        "page": "1"}
            yield FormRequest(self.comment_url, callback=self.parse_comment, method="GET", cookies=self.random_cookies(), formdata=formdata, meta={"formdata": formdata})

    def parse_comment(self, response):
        formdata = response.meta["formdata"]
        datapack = json.loads(response.body)
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

            # max_id = data["max_id"]
            # if max_id != 0:
            #     formdata["max_id"] = str(max_id)
            if page < data["max"]:
                formdata["page"] = str(page + 1)
                yield FormRequest(self.comment_url, callback=self.parse_comment, method="GET", cookies=self.random_cookies(), formdata=formdata, meta={"formdata": formdata})
        else:
            yield FormRequest(self.comment_url, callback=self.parse_comment, method="GET", cookies=self.random_cookies(), formdata=formdata)
