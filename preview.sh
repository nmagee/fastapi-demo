#!/bin/bash

cd app
/usr/bin/uvicorn main:app --reload --log-level debug
