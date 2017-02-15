# MongoDB experiments
To find efficiency gain by bulk queries over one by one query.
The motive behind this project is to find the exact efficiency gain by firing
bulk insert/update query over firing query one by one.

Findings of the experiment
-----------------------------------
1. Inserting data in bulk size of 500 is 10-15 time faster than inserting it one by one.
2. Updating data using BulkOperationBuilder in bulk of 500 is 3.4-4 time
faster than updating one by one

Table showing time required to insert 1,000,000 documents to empty mongoDB with given bulk size.
-----------------------------------

| bulk_size | time (sec)           |
|------|---------------|
| 1    | 270.89 |
| 2    | 148.56  |
| 4    | 88.51 |
| 8    | 60.78 |
| 16   | 42.19  |
| 32   | 31.66 |
| 64   | 25.24 |
| 128  | 22.67 |
| 256  | 21.24 |
| 512  | 20.64 |
| 1024 | 20.09  |


Table showing time required to update 100,000 documents in mongoDB with given bulk size.
-----------------------------------
| bulk_size    | time(sec)  |
|------|---------------|
| 1    | 46.47 |
| 2    | 29.66 |
| 4    | 20.41 |
| 8    | 15.35 |
| 16   | 12.73 |
| 32   | 10.78 |
| 64   | 10.01 |
| 128  | 9.58 |
| 256  | 9.47 |
| 512  | 9.27  |
| 1024 | 9.33 |
