#!/usr/bin/env python3
import json
import os
import mysql.connector
from mysql.connector import Error
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from pydantic import BaseModel

# FastAPI instance
app = FastAPI()

# CORS middleware to allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database configuration
DBHOST = "ds2022.cqee4iwdcaph.us-east-1.rds.amazonaws.com"
DBUSER = "admin"
DBPASS = os.getenv('DBPASS')
DB = "nem2p"  # You can modify this as needed, i.e., "vwr6nd" or "nem2p"

@app.get("/")  # Zone apex route
def zone_apex():
    return {"Good Day": "Sunshine!"}

@app.get('/genres')  # Endpoint to get genres from the database
async def get_genres():
    db = mysql.connector.connect(user=DBUSER, host=DBHOST, password=DBPASS, database=DB, ssl_disabled=True)
    cur = db.cursor()
    query = "SELECT * FROM genres ORDER BY genreid;"  # This is the correct query based on previous context
    try:
        cur.execute(query)
        headers = [x[0] for x in cur.description]  # Get column headers
        results = cur.fetchall()
        json_data = []
        for result in results:
            json_data.append(dict(zip(headers, result)))
        return json_data
    except Error as e:
        print("MySQL Error: ", str(e))
        return {"Error": "MySQL Error: " + str(e)}
    finally:
        cur.close()
        db.close()

@app.get('/songs')  # Endpoint to get songs along with genre information
async def get_songs():
    db = mysql.connector.connect(user=DBUSER, host=DBHOST, password=DBPASS, database=DB, ssl_disabled=True)
    cur = db.cursor()
    query = """
    SELECT songs.title, songs.album, songs.artist, songs.year, songs.file, songs.image, genres.genre
    FROM songs
    JOIN genres ON songs.genre = genres.genreid
    ORDER BY songs.title;
    """
    try:
        cur.execute(query)
        headers = [x[0] for x in cur.description]  # Get column headers
        results = cur.fetchall()
        json_data = []
        for result in results:
            json_data.append(dict(zip(headers, result)))
        return json_data
    except Error as e:
        print("MySQL Error: ", str(e))
        return None
    finally:
        cur.close()
        db.close()
