import requests
import pandas as pd
import TechNews_sql as sql
import TechNews_mongo as mg
from bs4 import BeautifulSoup

def request_html(_url):
    web = requests.get(_url)
    return BeautifulSoup(web.text, "html.parser")

url = 'https://technews.tw/'
soup = request_html(url)
dest = soup.select("div.topblack ul.screen li.block2014")

jdata = []
for li in dest:
    category = li.select_one("div.cat01").text
    
    sum_title = li.select_one("div.sum_title h3").text
    sum_title_url = li.select_one("a")['href']

    spotlist = li.select("li.spotlist")
    spotlist_l = []
    for spot in spotlist:
        title = spot.select_one("a").text
        url = spot.select_one("a")['href']
        spotlist_l.append({"title":title, "url":url})
    
    jdata.append({"category":category,
                 "sum_title":sum_title,
             "sum_title_url":sum_title_url,
                  "spotlist":spotlist_l})

df = pd.DataFrame.from_dict(jdata)
df.to_json('./exam1_1.json', orient='records', force_ascii=False)

sql.insert_technews(jdata)
mg.insert_technews(jdata)