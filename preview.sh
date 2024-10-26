#!/bin/bash

# Navigate to the app directory
cd app

# Run the FastAPI application with Uvicorn
uvicorn main:app --reload --log-level debug


