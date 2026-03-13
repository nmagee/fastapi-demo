#!/usr/bin/env python3

import json
import os
import logging
from fastapi import FastAPI, Request
import pymongo
from pymongo import MongoClient
from bson import ObjectId

MONGO_USERNAME = os.getenv('MONGO_USERNAME')
MONGO_PASSWORD = os.getenv('MONGO_PASSWORD')

client = MongoClient('mongodb://mongodb:27017/', username=MONGO_USERNAME, password=MONGO_PASSWORD)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")  # zone apex
def zone_apex():
    logger.info("Zone apex endpoint called")
    return {"Good Day": "Sunshine!"}

@app.get('/people')
async def get_people():
    # connect to a mongodb container running on localhost:27017
    db = client['nem2p']
    collection = db['people']
    people = collection.find()
    result = []
    for person in people:
        if '_id' in person:
            person['_id'] = str(person['_id'])
        result.append(person)
    logger.info(f"Found {len(result)} people")
    return result

@app.post('/people')
async def create_person(request: Request):
    data = await request.json()
    name = data['name']
    email = data['email']
    db = client['nem2p']
    collection = db['people']
    collection.insert_one({'name': name, 'email': email})
    logger.info(f"Person {name} created successfully")
    return {"message": f"Person {name} created successfully"}

@app.get('/people/delete/{person_id}')
async def delete_person(person_id: str):
    db = client['nem2p']
    collection = db['people']
    collection.delete_one({'_id': ObjectId(person_id)})
    logger.info(f"Person {person_id} deleted successfully")
    return {"message": f"Person {person_id} deleted successfully"}
