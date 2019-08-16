#! /bin/bash

# Simple script to grab the boid team leader board
# Requires a Bearer token for auth access
#
# You can grab your  bearer token with the script GrabMyToken.sh <boid-emailaddress> <password>


TOKEN="INSERT YOUR TOKEN HERE"
curl -qs -X POST https://api.boid.com/teamsLeaderboard -H "Authorization: Bearer $TOKEN" -H 'Content-Type: application/json' | python -m json.tool
