# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class UserItem(scrapy.Item):
    user_id = scrapy.Field()            # 用户id
    screen_name = scrapy.Field()        # 昵称
    statuses_count = scrapy.Field()     # 微博数
    verified = scrapy.Field()           # 是否认证
    verified_type = scrapy.Field()      # 认证类型
    verified_reason = scrapy.Field()    # 认证信息
    description = scrapy.Field()        # 简介
    gender = scrapy.Field()             # 性别
    urank = scrapy.Field()              # 微博等级
    mbrank = scrapy.Field()             # 微博会员等级
    follow_count = scrapy.Field()       # 关注数
    followers_count = scrapy.Field()    # 粉丝数

    created_at = scrapy.Field()         # 注册时间
    sunshine = scrapy.Field()           # 阳光信用
    birthday = scrapy.Field()           # 生日
    location = scrapy.Field()           # 所在地
    education = scrapy.Field()          # 教育经历
    company = scrapy.Field()            # 公司信息


class WeiboItem(scrapy.Item):
    user_id = scrapy.Field()            # 用户id
    weibo_id = scrapy.Field()           # 微博id
    text = scrapy.Field()               # 微博正文
    img = scrapy.Field()                # 图片url
    # video = scrapy.Field()              # 视频url
    # locate = scrapy.Field()             # 位置
    created_at = scrapy.Field()         # 日期
    tool = scrapy.Field()               # 工具
    reposts = scrapy.Field()            # 转发数
    comments = scrapy.Field()           # 点赞数
    attitudes = scrapy.Field()          # 点赞数
    original = scrapy.Field()           # 是否原创

    ouid = scrapy.Field()               # 源微博用户id
    owid = scrapy.Field()               # 源微博id
    otext = scrapy.Field()              # 源微博正文
    oimg = scrapy.Field()               # 源微博图片url
    # ovideo = scrapy.Field()             # 源微博视频url
    odate = scrapy.Field()              # 源微博日期
    otool = scrapy.Field()              # 源微博工具
    oreposts = scrapy.Field()           # 源微博转发数
    ocomments = scrapy.Field()          # 源微博评论数
    oattitudes = scrapy.Field()         # 源微博点赞数


class CommentItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    weibo_id = scrapy.Field()
    comment_id = scrapy.Field()
    user_id = scrapy.Field()
    screen_name = scrapy.Field()
    created_at = scrapy.Field()
    text = scrapy.Field()
    pic = scrapy.Field()
    like_count = scrapy.Field()