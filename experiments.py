'''
Code to find out efficiency gain by inseting/updating
data in bulk over inserting one by one
'''
import time
from pymongo import MongoClient

MONGO_SETTINGS = {'host': 'localhost', 'port': 27000}
MONGO_CLIENT = MongoClient(**MONGO_SETTINGS)
BULK_SIZE = 500
# BULK_SIZE size is chosed arbitrarily
# one can chose any thing by keeping mongo query size in limit

def insert_one_by_one(collection, num_rec):
    '''
    collection: mongoDb collection
    num_rec: number of records to be inserted
    this function inserts num_rec records to DB one by one
    and return the total time taken in the process
    '''
    start_time = time.time()
    for i in range(num_rec):
        data = {
            'userId': i
        }
        collection.insert(data)
    return time.time() - start_time

def insert_in_bulk(collection, num_rec):
    '''
    collection: mongoDb collection
    num_rec: number of records to be inserted
    this function inserts num_rec records to DB in bulk
    and return the total time taken in the process
    '''
    start_time = time.time()
    bulk_data = []
    for i in range(num_rec):
        data = {
            'userId': i
        }
        bulk_data.append(data)
        if len(bulk_data) == BULK_SIZE:
            collection.insert(bulk_data)
            bulk_data = []
    if len(bulk_data) > 0:
        collection.insert(bulk_data)
    return time.time() - start_time


def update_one_by_one(collection, num_rec):
    '''
    collection: mongoDb collection
    num_rec: number of records to be inserted
    this function first deletes all records in DB
    and inserts fresh num_rec records and then update it
    and returns the time taken while updating records and not total time
    '''
    collection.remove()
    insert_in_bulk(collection, num_rec)
    start_time = time.time()
    for i in range(num_rec):
        data = {
            'userId': str(i)
        }
        collection.update({'userId': i}, {'$set': data}, upsert=True)
    return time.time() - start_time

    
def update_in_bulk(collection, num_rec):
    '''
    collection: mongoDb collection
    num_rec: number of records to be inserted
    this function first deletes all records in DB
    and inserts fresh num_rec records and then update it in bulk
    and returns the time taken while updating records and not total time
    '''
    collection.remove()
    insert_in_bulk(collection, num_rec)
    bulk = collection.initialize_ordered_bulk_op()
    start_time = time.time()
    for i in range(num_rec):
        data = {
            'userId': str(i)
        }
        bulk.find({'userId': i}).upsert().update({'$set': data})
        if i % BULK_SIZE == 0:
            bulk.execute()
            bulk = collection.initialize_ordered_bulk_op()
    bulk.execute()
    return time.time() - start_time

if __name__ == "__main__":
    collection = MONGO_CLIENT['test_db'].profiles
    NUM_RECORDS = BULK_SIZE * 10
    time_to_insert_one_by_one = insert_one_by_one(collection, NUM_RECORDS)
    time_to_insert_in_bulk = insert_in_bulk(collection, NUM_RECORDS)
    one_by_one_update_time = update_one_by_one(collection, NUM_RECORDS)
    bulk_update_time = update_in_bulk(collection, NUM_RECORDS)
    insert_efficiency_factor = time_to_insert_one_by_one / time_to_insert_in_bulk
    update_efficiency_factor = one_by_one_update_time/bulk_update_time

    print 'Bulk insertion is [ {} ] time faster than one by one'.format(insert_efficiency_factor)
    print 'Bulk updation is [ {} ] time faster than one by one'.format(update_efficiency_factor)
