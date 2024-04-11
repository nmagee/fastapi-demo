import os
import MySQLdb
from pymongo import MongoClient

DBHOST = os.environ.get('DBHOST')
DBUSER = os.environ.get('DBUSER')
DBPASS = os.environ.get('DBPASS')
DB = "nem2p"

class mongo():
    # Set up normal Mongo Atlas connection + db + collection
    mongopass = os.getenv('MONGOPASS')
    uri = "mongodb+srv://cluster0.pnxzwgz.mongodb.net/"
    client = MongoClient(uri, username='nmagee', password=mongopass, connectTimeoutMS=200, retryWrites=True)
    db = client.nem2p
    hobbies = db.hobbies
