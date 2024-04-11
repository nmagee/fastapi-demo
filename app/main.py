#!/usr/bin/env python3

from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel
# from models import Item, Album
import json
import os
import MySQLdb
from fastapi.staticfiles import StaticFiles
import logging
import bson
from pymongo import MongoClient
from dbs import *


app = FastAPI()
app.mount("/static", StaticFiles(directory="static", html = True), name="static")


@app.get("/")  # zone apex
def zone_apex():
    return {"Hello": "Hello API", "album_endpoint":"/albums","static_endpoint":"/static","hobbies_endpoint":"/hobbies"}

@app.get("/albums")
def get_all_albums():
    db = MySQLdb.connect(host=DBHOST, user=DBUSER, passwd=DBPASS, db=DB)
    c = db.cursor(MySQLdb.cursors.DictCursor)
    c.execute("SELECT * FROM albums ORDER BY name")
    results = c.fetchall()
    db.close()
    return results

# get all hobbies
@app.get('/hobbies')
def get_hobbies():
    hobbies = mongo.db.hobbies.find({})
    results = []
    for hobby in hobbies:
        output = {}
        output['name'] = hobby['name']
        output['equipment']= hobby['equipment']
        results.append(output)
    return results


# @app.get("/albums/{id}")
# def get_one_album(id):
#     db = MySQLdb.connect(host=DBHOST, user=DBUSER, passwd=DBPASS, db=DB)
#     c = db.cursor(MySQLdb.cursors.DictCursor)
#     c.execute("SELECT * FROM albums WHERE id=" + id)
#     results = c.fetchall()
#     db.close()
#     return results
    