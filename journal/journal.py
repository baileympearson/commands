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

import pymongo

MongoClient = pymongo.MongoClient

''' 
TODO
	1. add a feature to allow the user to edit a past journal entry
	2. allow for accessing an entry by date
	3. allow user to set filename and location
	4. add password support
'''
class JournalEntry:
	def __init__(self,entry,date=datetime.datetime.now()):
		self.entry = entry
		self.date = date
	
	def __str__(self):
		coloredDate = colored(str(self.date),'red',attrs=[])
		return coloredDate + "\n" + self.entry
	
	@classmethod
	def init_from_dict(cls,dict):
		return cls(dict['entry'],dict['date'])

	def to_dict(self):
		return {
			'entry' : self.entry,
			'date' : self.date
		}
	
class Journal2:
	DB_NAME = 'journal-test'
	COLLECTION_NAME = 'entries'

	def __init__(self):
		self.client = MongoClient('mongodb://localhost:27017')
		self.db = self.client[self.DB_NAME]
		self.collection = self.db[self.COLLECTION_NAME]

	def add_entry(self,entry):
		''' 
		adds the specified entry into the database 
			entry: an instance of the JournalEntry class
		'''

		''' we don't even need to check if the entry
			exists in the database, since the db query
			includes a upsert=true field, which inserts
			the document if it does not exist '''
		
		# check if the entry exists in the database 
		res = self.collection.find_one({'date':entry.date})

		if res:
			self.update_entry(entry)
		else:
			self.collection.insert(entry.to_dict())
	
	def update_entry(self,entry):
		res = self.collection.update_one({'date':entry.date},{'$set': {'entry': entry.entry}},upsert=True)

	def delete_entry(self,date):
		''' Removes the entry with the particular date, if it exists. Else it does nothing '''
	
	def delete_all_entries(self):
		''' Clears the database. '''
		self.db.drop_collection(self.COLLECTION_NAME)
	
	def get_last_entry(self):
		''' Returns the last entry in the journal, sorted by date '''
		cursor = self.collection.find().sort('date',pymongo.DESCENDING)
		if cursor.count() > 0:
			return JournalEntry.init_from_dict(list(cursor)[0])

		return None
		
	def get_all_entries(self):
		''' Returns a list of all entries in the database ''' 
		cursor = self.collection.find()
		if cursor.count() > 0:
			return [JournalEntry.init_from_dict(item) for item in cursor]
		return None


class Journal():
	class JournalEntry():
		def __init__(self):
			self.entry = ''

			# get current date
			self.date = datetime.datetime.now().date()
		
		def __str__(self):
			coloredDate = colored(str(self.date),'red',attrs=[])
			return coloredDate + "\n" + self.entry
		
		def createEntry(self):
			self.entry = Journal().getEntryText()

		def appendEntry(self,rhs):
			self.entry += '\n' + rhs.entry


	file_name = "~/.journal-entries.pkl"
	def __init__(self):
		# expand the file path
		self.filename = os.path.expanduser(self.file_name)
		
		try:
			f = open(self.filename,'rb')
		except FileNotFoundError:
			create_file = input("Log file not be found.  Create new log file? [Y/N] ")
			create_file = create_file.strip().upper()
			if create_file != 'Y':
				click.echo("Exiting program.")
				sys.exit()

			# clearEntries will create a log file if none exists
			self.clearEntries()
			f = open(self.filename,'rb')

		try:
			self.data = pickle.load(f)
		except EOFError:
			self.data = None

		self.enable_color = True

	def addEntry(self):
		# are there any journal entries?
		if self.data is None:
			self.data = {}

		# create the journal entry
		entry = self.JournalEntry()
		entry.createEntry()

		# get the current time
		now = datetime.datetime.now().date()

		# check if we have a journal entry on the current date
		if now in self.data.keys():
			oldEntry = self.data[entry.date]
			oldEntry.appendEntry(entry)
		else:
			self.data[entry.date] = entry

	def listAllEntries(self):
		if not self.data:
			return ''

		ret = ''
		for item in sorted(self.data.keys()):
			ret += str(self.data[item]).strip() + "\n\n"
		return ret
	
	def getEntry(self,key):
		if self.data == None:
			return "No entries in journal."

		# get a random key
		return str(self.data[key])
	
	def save(self):
		f = open(self.filename,'wb')
		pickle.dump(self.data,f)
		f.close()
	
	def clearEntries(self):
		try:
			os.remove(self.filename)
		except OSError:
			pass
		open(self.filename,'w').close()

	def showLast(self):
		if not self.data:
			return 'No entries in journal'

		key = sorted(self.data.keys())[-1]
		return str(self.data[key])
	
	def chooseEntry(self,keys):
		i = 1
		for key in keys:
			s = str(i) + '. '
			s += str(key)
			print(s)
			i += 1

		choice = int(input("Choose entry: ").strip())
		if choice - 1 not in range(len(keys)):
			print('Entry out of range.')
			return None

		return keys[choice-1]
		
	def deleteEntry(self):
		keys = sorted(self.data.keys())

		choice = self.chooseEntry(keys)

		print()
		print(self.getEntry(choice))
		confirmation = input("\n\nAre you sure you wish to delete this entry? [Y/n] ").strip().upper()
		if confirmation[0] == 'Y':
			del self.data[choice]
	
	def getEntryText(self,entry = ''):
		EDITOR = os.environ.get('EDITOR') if os.environ.get('EDITOR') else 'vim'

		entry = bytes(entry,'utf-8')
		with tempfile.NamedTemporaryFile(suffix=".tmp") as tf:
			tf.write(entry)
			tf.flush()
			call([EDITOR,tf.name])

			tf.seek(0)
			edited_message = tf.read().decode('utf-8')
		return edited_message

	def show_last_entry(self):
		if self.data is None:
			sys.exit()

		key = sorted(self.data.keys())[-1]

		return self.getEntry(key)
	
	def editEntry(self,edit_last_entry):
		keys = sorted(self.data.keys())

		if not edit_last_entry:
			choice = self.chooseEntry(keys)
			if choice is None:
				return
		else:
			if keys == None:
				self.addEntry()
				return
			choice = keys[-1]

		entry = self.data[choice].entry

		new_entry = self.getEntryText(entry)
		self.data[choice].entry = new_entry
	
	def search(self,regex):
		matches = []

		for key in self.data.keys():
			res = regex.search(self.data[key].entry)
			if res is not None:
				matches.append(key)
		
		return [self.getEntry(key) for key in sorted(matches)]