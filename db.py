import datetime
import pymongo

#@todo rename database and create for a new item a new collection


try:
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    print("Connected successfully")
except:
    print("Couldnt connect to MongoDB")

db = client["amazon"]


def add_product_detail(details):
    new = db["products"]

    # extract ASIN from URL
    ASIN = details["url"][len(details["url"])-10:len(details["url"])]

    # try to store the data in DB
    try:
        details["date"] = datetime.datetime.now()
        new.update_one({"asin":ASIN}, {"$set": {"asin":ASIN}, "$push": {"details":details}}, upsert=True)
        return True
    except Exception as identifier:
        print(identifier)
        return False


def get_product_history(asin):
    new = db["products"]
    try:
        find = new.find_one({"asin": asin}, {"_id": 0})
        if find:
            return find
        else:
            raise Exception("Not found")
    except Exception as identifier:
        print(identifier)
        return None