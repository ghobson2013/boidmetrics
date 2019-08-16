#! /bin/bash

TOKEN="INSERT YOUR PERSONAL TOKEN HERE"

curl -qs -X POST https://api.boid.com/$1 -H "Authorization: Bearer $TOKEN"  | python -m json.tool

