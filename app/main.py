#!/usr/bin/env python3

from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel
from models import Item, Album
import json
import os
import MySQLdb
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.mount("/static", StaticFiles(directory="static", html = True), name="static")

# db config stuff
DBHOST = os.environ.get('DBHOST')
DBUSER = os.environ.get('DBUSER')
DBPASS = os.environ.get('DBPASS')
DB = "nem2p"

@app.get("/")  # zone apex
def zone_apex():
    return {"Hello": "Hello API", "album_endpoint":"/albums","static_endpoint":"/static"}



@app.get("/albums")
def get_all_albums():
    db = MySQLdb.connect(host=DBHOST, user=DBUSER, passwd=DBPASS, db=DB)
    c = db.cursor(MySQLdb.cursors.DictCursor)
    c.execute("SELECT * FROM albums ORDER BY name")
    results = c.fetchall()
    db.close()
    return results


# @app.get("/albums/{id}")
# def get_one_album(id):
#     db = MySQLdb.connect(host=DBHOST, user=DBUSER, passwd=DBPASS, db=DB)
#     c = db.cursor(MySQLdb.cursors.DictCursor)
#     c.execute("SELECT * FROM albums WHERE id=" + id)
#     results = c.fetchall()
#     db.close()
#     return results
    




# @app.post("/albums")
# def add_an_album(album: Album):
#     return {"name": album.name, "artist":album.artist, "genre": album.genre, "year":album.year}



# @app.post("/items/{item_id}")
# def add_item(item_id: int, item: Item):
#     return {"item_id": item_id, "item_name": item.name}

# @app.delete("/items/{item_id}")
# def delete_item(item_id: int, item: Item):
#     return {"action": "deleted", "item_id": item_id}

# @app.patch("/items/{item_id}")
# def patch_item(item_id: int, item: Item):
#     return {"action": "patch", "item_id": item_id}
