#!/usr/bin/env python3
import click
import datetime
import pickle
import random
import sys
import os
from termcolor import colored
import re
import sys, tempfile, os
from subprocess import call
import re

import pymongo

MongoClient = pymongo.MongoClient


from interface import Document

class Journal(Document):
	_DB_NAME =				'cli_apps'
	_COLLECTION_NAME =		'journal'
	_UPDATE_PARAMETER =		''
	_QUERY_PARAMETERS =		''
	_SORT_PARAMETER =		'date'

	date = datetime.datetime.now() 
	entry = ''

	def __str__(self):
		tmp_date = self.date.strftime("%B %d, %Y")
		coloredDate = colored(str(tmp_date),'red',attrs=[])
		return coloredDate + "\n" + self.entry
	

''' 
TODO
	1. add a feature to allow the user to edit a past journal entry
	2. allow for accessing an entry by date
	3. allow user to set filename and location
	4. add password support

	my_datetime.strftime("%B %d, %Y")
  
'''
class JournalEntry:
	def __init__(self,entry,date=datetime.datetime.now()):
		self.entry = entry
		self.date = date
	
	def __str__(self):
		tmp_date = self.date.strftime("%B %d, %Y")
		coloredDate = colored(str(tmp_date),'red',attrs=[])
		return coloredDate + "\n" + self.entry
	
	@classmethod
	def init_from_dict(cls,dict):
		return cls(dict['entry'],dict['date'])

	def to_dict(self):
		return {
			'entry' : self.entry,
			'date' : self.date
		}
	
"""	
class Journal:
	DB_NAME = 'journal'
	COLLECTION_NAME = 'entries'

	def __init__(self):
		self.client = MongoClient('mongodb://localhost:27017')
		self.db = self.client[self.DB_NAME]
		self.collection = self.db[self.COLLECTION_NAME]

	def add_entry(self,entry):
		''' 
		adds the specified entry into the database 
			@param entry: an instance of the JournalEntry class
		'''

		# check if the entry exists in the database 
		res = self.collection.find_one({'date':entry.date})

		if res:
			self.update_entry(entry)
		else:
			self.collection.insert(entry.to_dict())
	
	def match_entries(self,regex):
		'''
			returns a list of all JournalEntry entries that match the pattern regex
			if none exist, it returns None
				@param regex: a compiled regular expression pattern
		'''
		cursor = self.collection.find({'entry': regex})

		if cursor.count() > 0:
			return [JournalEntry.init_from_dict(item) for item in cursor]

		return None
	
	def update_entry(self,entry):
		'''
			Updates a particular entry in the journal.
		'''
		self.collection.update_one({'date':entry.date},{'$set': {'entry': entry.entry}},upsert=True)

	def delete_entry(self,date):
		''' 
			Removes the entry with the particular date, if it exists. Otherwise
			it does nothing.
		'''
		self.collection.delete_one({'date': date})
	
	def delete_all_entries(self):
		''' Removes all entries from the database. '''
		self.db.drop_collection(self.COLLECTION_NAME)
	
	def get_last_entry(self):
		''' Returns the last entry in the journal, sorted by date '''
		cursor = self.collection.find().sort('date',pymongo.DESCENDING)
		if cursor.count() > 0:
			return JournalEntry.init_from_dict(list(cursor)[0])

		return None
		
	def get_all_entries(self):
		''' 
			Returns a list of all entries in the database 
			If no entries exist, returns None.
		''' 
		cursor = self.collection.find()
		if cursor.count() > 0:
			return [JournalEntry.init_from_dict(item) for item in cursor]
		return None
	
	def get_count(self):
		cursor = self.collection.find()
		return cursor.count()

	"""	
