

#  Python Generators 

##  Project Overview

This project explores advanced usage of Python generators to efficiently process large datasets, simulate live data streaming, and perform memory-optimized computations.
It integrates (Python + SQL) to handle user data dynamically, demonstrating how generators improve performance by avoiding unnecessary memory consumption.


##  Learning Objectives

By completing this project, I learned to:

 ✅ Create and use Python generators with the yield keyword.
 ✅ Process large datasets iteratively without loading everything into memory.
 ✅ Implement batch processing and lazy loading for paginated data.
 ✅ Calculate aggregations (like averages) efficiently using generators.
 ✅ Integrate Python with MySQL using mysql.connector.



##  Project Structure

| File                      | Description                                                                               |
| ------------------------- | ----------------------------------------------------------------------------------------- |
| seed.py               | Creates the MySQL database ALX_prodev, table user_data, and inserts records from CSV. |
| 0-stream_users.py     | Implements a generator stream_users() that streams rows one by one from the database.   |
| 1-batch_processing.py | Implements batch generators to fetch and process users in chunks.                         |
| 2-lazy_paginate.py    | Implements a lazy pagination generator that loads each page on demand.                    |
| 4-stream_ages.py     | Streams user ages one by one and computes the average age efficiently.                    |


##  Installation and Setup

### 1. Clone the repository

bash
git clone https://github.com/<your-github-username>/alx-backend-python.git
cd alx-backend-python/python-generators-0x00


###  2. Install dependencies

Make sure you have Python 3 and MySQL installed, then install the connector:

bash
pip install mysql-connector-python


###  3. Configure MySQL credentials

Edit the connection details in each script:

python
user="root"
password="yourpassword"
host="localhost"


###  4. Run the setup script

bash
python3 seed.py


This will:

* Create the database ALX_prodev
* Create the user_data table
* Import data from user_data.csv


##  Usage Examples

### Stream users one by one

bash
python3 0-stream_users.py


###  Process users in batches

bash
python3 1-batch_processing.py


###  Lazy pagination

bash
python3 2-lazy_paginate.py


###  Average age (memory-efficient)

bash
python3 4-stream_ages.py




##  Key Takeaways

* Generators allow you to build pipelines for streaming data efficiently.
* Batch processing and lazy pagination prevent memory overload with large datasets.
* Combining Python generators + SQL queries makes real-time data streaming scalable.
