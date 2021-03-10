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
def insert_news_sql(df):
    sql = 'insert ignore into newsapi (sourceId, sourceName, author, title, description, url, urlToImage, publishedAt, content) values ("{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}")'
    with mysql() as cursor:
        for index,row in df.iterrows():
            print(row["source"]["id"])
            # print(index, sql.format(row["source"]["id"], row["source"]["id"], row["author"], row["title"], row["description"], row["url"], row["urlToImage"], row["publishedAt"].replace('T', ' ').replace('Z',''), row['content']))
            cursor.execute(sql.format(row["source"]["id"], row["source"]["name"], row["author"], row["title"], row["description"], row["url"], row["urlToImage"], row["publishedAt"].replace('T', ' ').replace('Z',''), row['content']))
        result = cursor.fetchall()
        # print(result)