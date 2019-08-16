#! /bin/bash


curl -qs -X POST https://api.boid.com/authenticateUser --data-binary '{"email": "'$1'", "password": "'$2'", "invitedById":null , "device":null }' -H "Content-type: application/json" -v #| python -m json.tool

