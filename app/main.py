#!/usr/bin/env python3

from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel
import requests
import json
import boto3

app = FastAPI()

# The URL for this API has a /docs endpoint that lets you see and test
# your various endpoints/methods.


# Model data you are expecting.
# Set defaults, data types, etc.
#
# Imagine the JSON below as a payload via POST method
# The endpoint can then parse the data by field (name, description, price, tax)
# {
#     "name":"Trek Domaine 5000",
#     "description": "Racing frame",
#     "price": 7200,
#     "tax": 381
# }

class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None


# Zone apex is the 'default' page for a URL
# This will return a simple hello world via GET method.
@app.get("/")  # zone apex
def read_root():
    return {"Hello": "World"}


# Adds two integers as PATH parameters
@app.get("/add/{number_1}/{number_2}")
def add_me(number_1: int, number_2: int):
    sum = number_1 + number_2
    return {"sum": sum}


# Introduce data types and defaults from the Optional library
@app.get("/items/{item_id}")
def read_items(item_id: int, q: str = None, s: str = None):
    # to-do: could be used to read from/write to database, use item_id as query parameter
    # and fetch results. The q and s URL parameters are optional.
    # - database
    # - flat text
    # - another api (internal)
    # - another api (external)
    return {"item_id": item_id, "q": q, "s": s}

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


@app.get("/github/repos/{user}")
def get_github_repos(user: str):
    url = "https://api.github.com/users/" + user + "/repos"
    response = requests.get(url)
    body = json.loads(response.text)
    return {"repos": body}


# Use another Py library to make an external API request.
# This is simpler than building the API call by hand using
# the `requests` library:
# @app.get("/aws/s3")
# def fetch_buckets():
#     s3 = boto3.client("s3")
#     response = s3.list_buckets()
#     buckets = response['Buckets']
#     return {"buckets": buckets}
