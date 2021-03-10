from selenium import webdriver
import pickle
import pymysql
import contextlib

# 定義上下文管理器，連線後自動關閉連線
@contextlib.contextmanager
def mysql(host='127.0.0.1', user='root', passwd='050949359', db='testdb'):
    conn = pymysql.connect(host=host, user=user, passwd=passwd, db=db)
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    try:
        yield cursor
    finally:
        conn.commit()
        cursor.close()
        conn.close()

def create_table():
    drop_sql = "drop table If Exists en_text;"
    create_sql = "create table en_text(en varchar(255));"
    with mysql() as cursor:
        cursor.execute(drop_sql)
        cursor.execute(create_sql)
        result = cursor.fetchall()

# 先在mysql內建立DB與table，再插入資料
def insert_text(text_list):
    sql = 'insert ignore into en_text values("{}");'
    with mysql() as cursor:
        for text in text_list:
            cursor.execute(sql.format(text))

        cursor.fetchall()

def write_to_txt(text_list):
    with open("./exam_3.txt", "w") as file:
        for text in text_list:
            file.write(text+"\n")

def write_to_pk(text_list):
    with open("./exam_3.pk", "wb") as file:
        pickle.dump(text_list, file)

driver = webdriver.PhantomJS("./phantomjs")
driver.get('https://gogakuru.com/english/phrase/genre/180_%E5%88%9D%E7%B4%9A%E3%83%AC%E3%83%99%E3%83%AB.html?layoutPhrase=1&orderPhrase=1&condMovie=0&flow=enSearchGenre&condGenre=180&perPage=50')
target_list = driver.find_elements_by_css_selector(".item_type01 .summary dd a span")

text_list = []
for element in target_list:
    print(element.text)
    text_list.append(element.text)

write_to_txt(text_list)

create_table()
insert_text(text_list)

write_to_pk(text_list)

driver.quit()