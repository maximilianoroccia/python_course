#from pymongo import MongoClient

#db_client = MongoClient().local

# Base de datos remota

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# pass: maxidev2026

uri = "mongodb+srv://mxeroccia_db_user:maxidev2026@cluster0.d2oo9qb.mongodb.net/?appName=Cluster0"

# Create a new client and connect to the server
db_client = MongoClient(uri, server_api=ServerApi('1')).test

# Send a ping to confirm a successful connection
try:
    db_client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
