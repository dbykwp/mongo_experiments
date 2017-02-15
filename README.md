# mongo_experiments
To find efficiency gain by bulk queries over one by one query
The motive behind this project is to find the exact efficiency gain by firing bulk insert/update query over firing query one by one.
Finding out of the experiment
-----------------------------------
1. Inserting data in bulk size of 500 is 10-15 time faster than inserting it one by one.
2. Updating data using BulkOperationBuilder in bulk of 500 is 3.4-4 times faster than updating one by one
