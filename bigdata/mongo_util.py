# encoding=utf-8
from pymongo import MongoClient

client = MongoClient()
db = client.primer


def test():
    db.tickets.insert({
        "hello": "world"
    })
    cursor = db.tickets.find()
    for document in cursor:
        print(document)


def insert_one(json):
    try:
        db.tickets.insert(json)
    except:
        print "insert one failed"


if __name__ == '__main__':
    test()
