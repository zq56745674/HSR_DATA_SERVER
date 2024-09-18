import pymongo

def get_mongo_client():
    return pymongo.MongoClient("mongodb://localhost:27017/")

def get_mongo_db(db_name):
    client = get_mongo_client()
    return client[db_name]

def get_mongo_collection(db_name, collection_name):
    db = get_mongo_db(db_name)
    return db[collection_name]

def insert_one_document(db_name, collection_name, document):
    collection = get_mongo_collection(db_name, collection_name)
    return collection.insert_one(document)

def insert_many_documents(db_name, collection_name, documents):
    collection = get_mongo_collection(db_name, collection_name)
    return collection.insert_many(documents)

if __name__ == "__main__":
    client = get_mongo_client()
    print(client.list_database_names())
    db = get_mongo_db("test")
    print(db.list_collection_names())
    collection = get_mongo_collection("test", "hsrdata")
    print(collection.find_one())

    document = {"name": "John", "age": 30}
    insert_one_document("test", "hsrdata", document)
    print(collection.find_one())
    client.close()