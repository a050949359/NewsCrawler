from pymongo import MongoClient
import pandas

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