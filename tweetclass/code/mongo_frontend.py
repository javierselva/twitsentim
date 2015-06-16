import json
import pymongo

'''
Code extract from the book " Mining the Social Web, Matthew A. Russell - 2nd Edition.
It is used to save tweets in a MongoDb database.
'''

def save_to_mongo(data, mongo_db,mongo_db_coll, **mongo_conn_kw):
    
    # Connects to the MongoDB server running on 
    # localhost:27017 by default
    
    client = pymongo.MongoClient(**mongo_conn_kw)
    
    # Get a reference to a particular database
    
    db = client[mongo_db]
    
    # Reference a particular collection in the database

    coll = db[mongo_db_coll]
    
    # Perform a bulk insert and  return the IDs
    
    return coll.insert(data)

def load_from_mongo(mongo_db,mongo_db_coll,return_cursor=False,criteria=None,projection=None,**mongo_conn_kw):
    # Optionally, use criteria and projection to limit the data that is 
    # returned as documented in 
    # http://docs.mongodb.org/manual/reference/method/db.collection.find/
    # Consider leveraging MongoDB's aggregations framework for more 
    # sophisticated queries.
    
    client=pymongo.MongoClient(**mongo_conn_kw)
    db = client[mongo_db]
    coll = db[mongo_db_coll]

    if criteria is None:
        criteria={}
    if projection is None:
        cursor=coll.find(criteria)
    else:
        cursor=coll.find(criteria,projection)
    
    # Returning a cursor is recommended for large amounts of data
    
    if return_cursor:
        return cursor
    else:
        return [ item for item in cursor ]
