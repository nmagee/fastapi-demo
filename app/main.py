#!/usr/bin/env python3

from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel
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

# More will go here TBD