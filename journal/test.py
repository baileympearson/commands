#!/usr/bin/env python3
import re
from termcolor import colored
import os

import sys, tempfile, os
from subprocess import call

from pprint import pprint

# import the mongodb client
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017')

db = client['heroapp']
collection = db['heroes']

pprint(collection.find({'name':'bailey'}))

hero = {
	'name': 'bailey',
	'age': 21,
	'type':'student',
}

res = collection.find({'type':'student'})
for item in res:
	print(item)

import datetime
class Entry:

	def __init__(self,entry=''):
		self.entry = entry
		self.date = datetime.datetime.now()
	
	def to_dict(self):
		return {
			'entry': self.entry,
			'date':self.date
		}

today = Entry('Hello world from my app!')
collection.insert_one(today.to_dict())

for item in collection.find():
	pprint(item)