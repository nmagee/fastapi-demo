#!/usr/bin/env python3

from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel
import json
import os

app = FastAPI()

@app.get("/")  # zone apex
def zone_apex():
    return {"Hello": "Hello Ryan"}

@app.get("/add/{a}/{b}")
def add(a: int, b: int):
    return {"sum": a + b}

@app.get("/multiply/{c}/{d}")
def multiply(c: int, d: int):
    return {"product": c * d}


@app.get("/square/{e}")
def square(e: int):
    return {"square": e * e}

@app.get("/loop/{f}")
def loop(f: int):
    empt = ""
    for i in range(f):
        empt+=str(i)
        
    return {empt}