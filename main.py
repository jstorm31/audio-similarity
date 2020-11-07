#!/usr/bin/env python3

# import the MongoClient class
from pymongo import MongoClient, errors
import os
from dotenv import load_dotenv

load_dotenv()

# use a try-except indentation to catch MongoClient() errors
try:
    # try to instantiate a client instance
    client = MongoClient(
        host=[str(os.getenv('MONGO_DOMAIN')) + ":" +
              str(os.getenv('MONGO_PORT'))],
        serverSelectionTimeoutMS=10000,
        username=os.getenv('MONGO_INITDB_ROOT_USERNAME'),
        password=os.getenv('MONGO_INITDB_ROOT_PASSWORD'),
    )

    # print the version of MongoDB server if connection successful
    print("server version:", client.server_info()["version"])

    # get the database_names from the MongoClient()
    database_names = client.list_database_names()

except errors.ServerSelectionTimeoutError as err:
    # set the client and DB name list to 'None' and `[]` if exception
    client = None
    database_names = []

    # catch pymongo.errors.ServerSelectionTimeoutError
    print("pymongo ERROR:", err)

print("\ndatabases:", database_names)
