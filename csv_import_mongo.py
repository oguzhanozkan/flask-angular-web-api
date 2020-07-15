import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["RssFeedApiDatabase"]
mycol = mydb["rssFeed"]

def insert_data(data):
    s = data.to_dict('records')
    mycol.insert_many(s)
