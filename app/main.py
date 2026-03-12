#!/usr/bin/env python3

import logging
import os
from contextlib import asynccontextmanager

from bson import ObjectId
from fastapi import FastAPI, Request, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from pymongo.errors import PyMongoError

# Configuration
MONGO_USERNAME = os.getenv('MONGO_USERNAME')
MONGO_PASSWORD = os.getenv('MONGO_PASSWORD')
MONGO_URI = 'mongodb://mongodb:27017/'

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global client reference
mongo_client = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage MongoDB connection lifecycle"""
    global mongo_client
    # Startup: Connect to MongoDB
    try:
        mongo_client = MongoClient(
            MONGO_URI,
            username=MONGO_USERNAME,
            password=MONGO_PASSWORD,
            serverSelectionTimeoutMS=5000
        )
        # Test connection
        mongo_client.admin.command('ping')
        logger.info("Successfully connected to MongoDB")
    except PyMongoError as e:
        logger.error(f"Failed to connect to MongoDB: {e}")
        raise

    yield

    # Shutdown: Close MongoDB connection
    if mongo_client:
        mongo_client.close()
        logger.info("MongoDB connection closed")


app = FastAPI(lifespan=lifespan)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_collection(db_name: str, collection_name: str):
    """Helper function to get MongoDB collection"""
    if mongo_client is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database connection not available"
        )
    return mongo_client[db_name][collection_name]


@app.get("/")
def zone_apex():
    """Health check endpoint"""
    logger.info("Zone apex endpoint called")
    return {"Good Day": "Sunshine!"}


@app.get('/people')
async def get_people():
    """Retrieve all people from the database"""
    try:
        collection = get_collection('nem2p', 'people')
        # Use list comprehension instead of for-loop for efficiency
        people = [
            {**person, '_id': str(person['_id'])}
            for person in collection.find()
        ]
        logger.info(f"Found {len(people)} people")
        return people
    except PyMongoError as e:
        logger.error(f"Database error retrieving people: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve people"
        )


@app.post('/people')
async def create_person(request: Request):
    """Create a new person"""
    try:
        data = await request.json()

        # Validate required fields
        if 'name' not in data or 'email' not in data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Name and email are required"
            )

        collection = get_collection('nem2p', 'people')
        result = collection.insert_one({
            'name': data['name'],
            'email': data['email']
        })

        logger.info(f"Person {data['name']} created with ID {result.inserted_id}")
        return {
            "message": "Person created successfully",
            "id": str(result.inserted_id)
        }
    except PyMongoError as e:
        logger.error(f"Database error creating person: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create person"
        )


@app.delete('/people/{person_id}')
async def delete_person(person_id: str):
    """Delete a person by ID"""
    try:
        # Validate ObjectId format
        try:
            obj_id = ObjectId(person_id)
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid person ID format"
            )

        collection = get_collection('nem2p', 'people')
        result = collection.delete_one({'_id': obj_id})

        if result.deleted_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Person with ID {person_id} not found"
            )

        logger.info(f"Person {person_id} deleted successfully")
        return {"message": "Person deleted successfully"}
    except HTTPException:
        raise
    except PyMongoError as e:
        logger.error(f"Database error deleting person: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete person"
        )
