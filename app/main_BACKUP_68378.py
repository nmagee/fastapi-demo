#!/usr/bin/env python3
import mysql.connector
from mysql.connector import Error
from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel
import json
import os

app = FastAPI()

DBHOST = "ds2022.cqee4iwdcaph.us-east-1.rds.amazonaws.com"
DBUSER = "admin"
DBPASS = os.getenv('DBPASS')
DB = "vwr6nd"

app = FastAPI()
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/genres')
def get_genres():
<<<<<<< HEAD
    db = mysql.connector.connect(user=DBUSER, host=DBHOST, password=DBPASS, database=DB)
    cur=db.cursor()
    query = "SELECT * FROM genres ORDER BY genreid;"
=======
    query = "SELECT * FROM genres ORDER BY reid;"
>>>>>>> e0d3e968854ca34f608b51b057ec002f75347549
    try:    
        cur.execute(query)
        headers=[x[0] for x in cur.description]
        results = cur.fetchall()
        json_data=[]
        for result in results:
            json_data.append(dict(zip(headers,result)))
        return(json_data)
    except Error as e:
        return {"Error": "MySQL Error: " + str(e)}
<<<<<<< HEAD
    finally:
        cur.close()
        db.close()
    
@app.get('/songs')
def get_songs():
    db = mysql.connector.connect(user=DBUSER, host=DBHOST, password=DBPASS, database=DB)
    cur=db.cursor()
    query = "SELECT songs.title, songs.album, songs.artist, songs.year, songs.file, genres.genre FROM `songs` JOIN genres ON genres.genreid = songs.genre;"
    try:    
        cur.execute(query)
        headers = [x[0] for x in cur.description]  # column headers
        results = cur.fetchall()
        json_data = []
        for result in results:
            json_data.append(dict(zip(headers, result)))
        return json_data
    except Error as e:
        return {"Error": "MySQL Error: " + str(e)}
    finally:
        cur.close()
        db.close()

# Connect to the database

=======
    
@app.get('/songs')
def get_songs():
    query = "SELECT songs.title, songs.album, songs.artist, songs.year, songs.file, genres.genre FROM `songs` JOIN genres ON genres.genreid = songs.genre;;"
    try:    
        cur.execute(query)
        headers=[x[0] for x in cur.description]
        results = cur.fetchall()
        json_data=[]
        for result in results:
            json_data.append(dict(zip(headers,result)))
        return(json_data)
    except Error as e:
        return {"Error": "MySQL Error: " + str(e)}
    
db = mysql.connector.connect(user=DBUSER, host=DBHOST, password=DBPASS, database=DB)
cur=db.cursor()
# Connect to the database
>>>>>>> e0d3e968854ca34f608b51b057ec002f75347549
