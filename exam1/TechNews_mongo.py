from pymongo import MongoClient
import pandas as pd

# import 聯合 的資料 
def insert_technews(data):
    client = MongoClient('mongodb://192.168.56.102:27017/')
    db = client["assignment"]
    col = db["technews"]
    # print(list(col.find({},{'_id':0,'sum_title':1})))
    df = pd.DataFrame(col.find({},{'_id':0,'sum_title':1}))
    if df.empty:
        col.insert_many(data)
    else:
        for news in data:
            if not df['sum_title'].str.contains(news['sum_title']).any():
                col.insert_one(news)

def insert_sum_content(data):
    client = MongoClient('mongodb://192.168.56.102:27017/')
    db = client["assignment"]
    col = db["technews"]
    query = { "sum_title": data['title'] }
    newvalues = { "$set": { "content": data['content'] } } 
    col.update(query, newvalues)

def insert_spot_content(data):
    client = MongoClient('mongodb://192.168.56.102:27017/')
    db = client["assignment"]
    col = db["technews"]
    
    spot_title_key = "spotlist"+'.'+str(data['index'])+'.'+"title"
    query = {spot_title_key: data['title']}
    
    spot_content_key = "spotlist"+'.'+str(data['index'])+'.'+"content"
    newvalues = { "$set": { spot_content_key: data['content'] } } 
    col.update(query, newvalues)