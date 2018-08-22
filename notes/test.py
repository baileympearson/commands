#!/usr/bin/env python3
import re
from termcolor import colored
import os

import sys, tempfile, os
from subprocess import call

from pprint import pprint

import pymongo 

# import the mongodb client
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017')

db = client['journal-test']
collection = db['entries']


def insert_test_data():
	def rand_date():
		from datetime import datetime
		import random
		
		year = random.randint(1950, 2000)
		month = random.randint(1, 12)
		day = random.randint(1, 28)
		birth_date = datetime(year, month, day)
		return birth_date

	entries = [{'entry':'banana!','date': rand_date()} for i in range(5)]
	return entries
entries = insert_test_data()

collection.insert_many(entries)

import re
regx = re.compile("a!", re.IGNORECASE)

cursor = collection.find({"entry": regx})

for item in cursor:
	print(item)
