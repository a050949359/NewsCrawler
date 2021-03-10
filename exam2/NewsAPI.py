from newsapi import NewsApiClient
import pandas
import json
import NewsAPI_sql as ns
import NewsAPI_mongo as nm

def insert_news_mongo(df):
    client = MongoClient('mongodb://192.168.56.102:27017/')
    db = client["assignment"]
    col = db["newsapi"]
    # print(list(col.find({},{'_id':0,'sum_title':1})))
    json_data = eval(df.to_json(orient='records', force_ascii=False).replace("null","'null'"))
    
    df = pandas.DataFrame(col.find({},{'_id':0,'sum_title':1}))
    
    if df.empty:
        col.insert_many(json_data)
    else:
        for news in json_data:
            if not df['sum_title'].str.contains(news['sum_title']).any():
                col.insert_one(news)

# Init
newsapi = NewsApiClient(api_key='10a72a45c8ec4cdb89dec1a9d289feb3')

# /v2/everything
all_articles = newsapi.get_everything(q='武漢肺炎 AND NOT 外遇',
                                      domains='udn.com,chinatimes.com,storm.mg,ettoday.net',
                                      sort_by='publishedAt',
                                      page_size=100)
articles = all_articles['articles']
# df = pandas.DataFrame(articles)
# # pandas.DataFrame.to_json()
# news_json = df.to_json(orient='records', force_ascii=False)

with open('./exam2.json','w+') as file:
    for i,news in enumerate(articles):
        if i == 0:
            file.write(json.dumps(news, ensure_ascii=False))
        else:
            file.write(',\n' + json.dumps(news, ensure_ascii=False))

with open('./exam2.json') as file:
    json_file = file.read()

df = pandas.read_json('['+json_file+']')
ns.insert_news_sql(df)
nm.insert_news_mongo(df)
