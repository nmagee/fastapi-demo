#!/usr/bin/env python3

from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel
import json
import os

app = FastAPI()

@app.get("/")  # zone apex
def zone_apex():
    return {"Hello": "Hello Aanaya"}

@app.get("/add/{a}/{b}")
def add(a: int, b: int):
    return {"sum": a + b}
@app.get("/square/{a}")
def get_square(a: int):
    return{"result":a ** 2}


