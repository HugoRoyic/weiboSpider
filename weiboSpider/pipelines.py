# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import sqlite3
from .items import UserItem, WeiboItem, CommentItem
from settings import SQLITE_PATH

class WeibospiderPipeline:
    def __init__(self):
        self.con = sqlite3.connect(SQLITE_PATH)
        self.cur = self.con.cursor()
        self.create_table()

    def create_table(self):
        self.cur.executescript("""
        CREATE TABLE IF NOT EXISTS user(
            user_id VARCHAR(32) NOT NULL,
            screen_name VARCHAR(64) NOT NULL,
            statuses_count INTEGER,
            verified INTEGER,
            verified_type INTEGER,
            verified_reason VARCHAR(32),
            description VARCHAR(140),
            gender VARCHAR(4),
            urank INTEGER,
            mbrank INTEGER,
            follow_count INTEGER,
            followers_count INTEGER,
            created_at VARCHAR(32),
            sunshine VARCHAR(32),
            birthday VARCHAR(32),
            location VARCHAR(32),
            education VARCHAR(32),
            company VARCHAR(32),
            PRIMARY KEY (user_id)
            );
        CREATE TABLE IF NOT EXISTS weibo (
            user_id VARCHAR(32) NOT NULL,
            weibo_id VARCHAR(32) NOT NULL,
            text TEXT,
            img TEXT,
            created_at VARCHAR(32),
            tool VARCHAR(32),
            reposts INTEGER,
            comments INTEGER,
            attitudes INTEGER,
            original INTEGER,
            ouid VARCHAR(32),
            owid VARCHAR(32),
            otext TEXT,
            oimg TEXT,
            odate VARCHAR(32),
            otool VARCHAR(32),
            oreposts INTEGER,
            ocomments INTEGER,
            oattitudes INTEGER,
            PRIMARY KEY (weibo_id)
            );
        CREATE TABLE IF NOT EXISTS comment (
            weibo_id VARCHAR(32) NOT NULL,
            comment_id VARCHAR(32) NOT NULL,
            user_id VARCHAR(32) NOT NULL,
            screen_name VARCHAR(64) NOT NULL,
            created_at VARCHAR(32),
            text TEXT,
            pic TEXT,
            like_count INTEGER,
            PRIMARY KEY (comment_id)
            ) """)

    def process_item(self, item, spider):
        if isinstance(item, UserItem):
            tablename = "user"
        elif isinstance(item, WeiboItem):
            tablename = "weibo"
        elif isinstance(item, CommentItem):
            tablename = "comment"

        keys = ','.join(item.keys())
        values = ','.join(["?"] * len(item))
        self.cur.execute(f"""INSERT OR IGNORE INTO {tablename} ({keys}) VALUES ({values})""", tuple(item.values()))
        self.con.commit()

    def close_spider(self, spider):
        self.con.close()