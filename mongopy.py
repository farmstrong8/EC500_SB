from pymongo import MongoClient
import os
import json
def main():
    client = MongoClient()
    client = MongoClient('localhost', 27017)
    db = client.pymongo_test
    record = db.pymongo_test_collection
    page = open('airports.json', 'r')
    parsed = json.loads(page.read())

    for item in parsed:
        record.insert(item)


if __name__=='__main__':
    main()
