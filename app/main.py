#!/usr/bin/env python3

from fastapi import Request, FastAPI
from typing import Optional
from pydantic import BaseModel
import json
import os
import mysql.connector
from mysql.connector import Error


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
    return {"Hello": "Hello API"}

@app.get("/add/{a}/{b}")
def add(a: int, b: int):
    return {"sum": a + b}

#@app.get("/customer/{idx}")
#def get_customer(idx: int):
    #get the data
    df = pd.read_csv("../customers.csv")
    #filter the data by index
    customer = df.iloc[idx]
    #the output is the customer that we found, so we are making it a dictionary
    return customer.to_dict()

#@api.get("/get_payload/{idx}")
#async def get_payload(request: Request): #async and await are little markers telling the system that it is ok if the system takes a sec
    #response = await request.json()
    #geo = response.get("geo")
    #url = "https://maps.google.com/?q={geo}".format(geo = geo)

    #return await request.json



DBHOST = "ds2022.cqee4iwdcaph.us-east-1.rds.amazonaws.com"
DBUSER = "admin"
DBPASS = os.getenv('DBPASS')
DB = "jph4dg"

db = mysql.connector.connect(user=DBUSER, host=DBHOST, password=DBPASS, database=DB)
cur=db.cursor()


@app.get('/genres')
def get_genres():
    query = "SELECT * FROM genres ORDER BY genreid;"
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

@app.get('/songs')
def get_songs():
    query = "SELECT songs.title, songs.album, songs.artist, songs.year, songs.file, songs.image, genres.genre FROM songs JOIN genres ON songs.genre = genres.genreid;"
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

