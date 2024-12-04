#!/usr/bin/env python3

from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel
import json
import os

app = FastAPI()

@app.get("/")  # zone apex
def zone_apex():
    return {"Hello friend!": "Howdy pal!"}

@app.get("/add/{a}/{b}")
def add(a: int, b: int):
    return {"sum": a + b} 

@app.get("/multiply/{c}/{d}")
def multiply(c: int, d: int):  # Corrected function name and removed extra brace
    return {"product": c * d}

@app.get("/divide/{g}/{h}")
def divide(g: int, h: int):  # Removed extra brace
    return {"quotient": g / h}
