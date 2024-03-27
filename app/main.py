#!/usr/bin/env python3

from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel
from models import Item, Album
import json
import requests
import boto3

import os
import MySQLdb
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

HOST = os.environ.get('DBHOST')
USER = os.environ.get('DBUSER')
PASS = os.environ.get('DBPASS')

# The URL for this API has a /docs endpoint that lets you see and test
# your various endpoints/methods.

@app.get("/")  # zone apex
def zone_apex():
    return {"Hello": "Hello World"}

@app.get("/albums")
def get_albums():
    db = MySQLdb.connect(host=HOST, user=USER, passwd=PASS, db="nem2p")
    c = db.cursor(MySQLdb.cursors.DictCursor)
    c.execute("""SELECT * FROM albums ORDER BY name LIMIT 20""")
    results = c.fetchall()
    albums = []
    content = {}
    for result in results:
        content = {"name": result['name'], "artist":result['artist'], "genre":result['genre'], "year":result['year']}
        albums.append(content)
        content = {}
    c.close()
    db.close()
    return albums

@app.post("/submit")
def submit_them(album: Album):
    return {"artist": album.artist, "band": album.title}

# Start using the "Item" BaseModel
# Post / Delete / Patch methods
@app.post("/items/{item_id}")
def add_item(item_id: int, item: Item):
    return {"item_id": item_id, "item_name": item.name}

@app.delete("/items/{item_id}")
def delete_item(item_id: int, item: Item):
    return {"action": "deleted", "item_id": item_id}

@app.patch("/items/{item_id}")
def patch_item(item_id: int, item: Item):
    return {"action": "patch", "item_id": item_id}


# api calls within an api!
@app.get("/github/repos/{user}")
def github_user_repos(user):
    url = "https://api.github.com/users/" + user + "/repos"
    response = requests.get(url)
    body = json.loads(response.text)
    return {"repos": body}

# Incorporate with boto3: simpler than the `requests` library:
@app.get("/aws/s3")
def fetch_buckets():
    s3 = boto3.client("s3")
    response = s3.list_buckets()
    buckets = response['Buckets']
    return {"buckets": buckets}
