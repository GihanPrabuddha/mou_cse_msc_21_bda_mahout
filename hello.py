#!/usr/bin/python
# -*- coding: utf-8 -*-
from klein import run, route
import redis
import os

# Start up a Redis instance

r = redis.StrictRedis(host='localhost', port=6379, db=0)

# Pull out all the recommendations from HDFS

p = os.popen('hadoop fs -cat recommendations/part*')

# Load the recommendations into Redis

for i in p:

  # Split recommendations into key of user id
  # and value of recommendations
  # E.g., 35^I[2067:5.0,17:5.0,1041:5.0,2068:5.0,2087:5.0,
  #       1036:5.0,900:5.0,1:5.0,081:5.0,3135:5.0]$

    (k, v) = i.strip().split('\t')

  # Put key, value into Redis

    r.set(k, v)
    print r


# Establish an endpoint that takes in user id in the path

@route('/<string:id>')
def recs(request, id):
    print id

    # Get recommendations for this user

    v = r.get(id)
    print v
    return 'The recommendations for user ' + id + ' are ' \
        + v.decode('utf-8')


# Make a default endpoint

@route('/')
def home(request):
    return 'Please add a user id to the URL, e.g. http://localhost:8082/30'

# Start up a listener on port 8082

run('localhost', 8082)
