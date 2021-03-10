import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import TechNews_sql as sql
import TechNews_mongo as mg

def get_news_content(url):
    html = requests.get(url)
    soup = BeautifulSoup(html.text, 'html.parser')
    return soup.select_one('div.content div.indent')
    
# 把Ｐ標籤底下有Strong的Ｐ標籤移除
def extract_p_strong(content):
    for tag in content.findAll(['p','h3']):
        if(tag.name == 'p'):         
            for strong in tag.findAll('strong'):
                strong.extract()

# sum的檔案名稱
def get_sum_file_name(df, i):
    return './'+'sum_'+df['category'][i]+'_'+str.replace(df['sum_title'][i][0:4], " ", "_")+'.txt'

# spot的檔案名稱
def get_spot_file_name(df, i, j):
    return './'+'spot_'+df['category'][i]+'_'+str.replace(df['spotlist'][i][j]['title'][0:4], " ", "_")+'.txt'

# 寫入檔案
def write_to_file(file_name):
    _content = ""
    with open(file_name, 'w') as file:
        for tag in content.findAll(['p','h3']):
            file.write(tag.text+'\n')
            _content += tag.text+'\n'

    return _content

#main1_2 start
df = pd.read_json('./exam1_1.json')

# 存sum的檔案
for i,url in enumerate(df['sum_title_url']):
    time.sleep(2)
    content = get_news_content(url)
    extract_p_strong(content)
    
    file_name = get_sum_file_name(df, i)
    print('write news to',file_name)
    # file
    content = write_to_file(file_name)
    # mysql
    sql.insert_news_content({"title":df['sum_title'][i], "content":content})
    # mongodb
    mg.insert_sum_content({"title":df['sum_title'][i], "content":content})

# 存spot的檔案
for i,spotlist in enumerate(df['spotlist']):
    for j,spot in enumerate(spotlist):
        time.sleep(2)
        content = get_news_content(spot['url'])
        extract_p_strong(content)
        
        file_name = get_spot_file_name(df, i, j)
        print('write news to',file_name)
        # file
        content = write_to_file(file_name)
        # mysql
        sql.insert_news_content({"title":df['spotlist'][i][j]['title'], "content":content})
        # mongodb
        mg.insert_spot_content({"title":df['spotlist'][i][j]['title'], "content":content, "index":j})
    