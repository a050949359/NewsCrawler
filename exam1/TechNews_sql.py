import pymysql
import contextlib

# 定義上下文管理器，連線後自動關閉連線
@contextlib.contextmanager
def mysql(host='192.168.56.102', user='harold', passwd='123456', db='assignment'):
    conn = pymysql.connect(host=host, user=user, passwd=passwd, db=db)
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    try:
        yield cursor
    finally:
        conn.commit()
        cursor.close()
        conn.close()
        
# 先在mysql內建立DB與table，再插入資料
def insert_technews(data):
    sql = "insert ignore into technews values('{}', {}, '{}', '{}');"
    with mysql() as cursor:
        for i in range(len(data)):
            news_category = data[i]["category"]
            news_type =  0
            news_title = data[i]["sum_title"]
            news_url = data[i]["sum_title_url"]
            cursor.execute(sql.format(news_category, news_type, news_title, news_url))

            for j in range(len(data[i]['spotlist'])):
                news_type =  1
                news_title = data[i]["spotlist"][j]["title"]
                news_url = data[i]["spotlist"][j]["url"]
                cursor.execute(sql.format(news_category, news_type, news_title, news_url))

        result = cursor.fetchall()
        print(result)

def insert_news_content(data):
    sql = "insert ignore into news_content values('{}', '{}');"
    with mysql() as cursor:
        cursor.execute(sql.format(data["title"], data["content"]))
        result = cursor.fetchall()