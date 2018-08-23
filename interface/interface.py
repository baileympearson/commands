#! /usr/bin/python3
from abc import ABCMeta, abstractmethod,ABC

import datetime
import inspect
import pymongo
MongoClient = pymongo.MongoClient

class Document(ABC):
	''' Responsible for all group level operations. '''
	@classmethod
	def get(cls,pk):
		''' Returns the pk'th document in the database '''
		obj = cls()
		ret = obj._collection.find({'id' : pk})

		if ret.count() == 0:
			raise IndexError("object requested does not exist")
			# here we need to construct the object and return it

		params = obj.get_properties()
		for item in params:
			obj.__dict__[item] = ret[0][item]

		return obj
		

	@classmethod
	def all(cls):
		''' Returns a list of all the documents in 
		the database '''
		# return self._collection.find()
		obj = cls()

		ret = obj._collection.find()
		
		if ret.count() == 0:
			return []

		params = obj.get_properties()

		documents = []
		for item in ret:
			tmp = cls()
			for param in params:
				tmp.__dict__[param] = item[param]
			documents.append(tmp)
		return documents

	@classmethod
	def get_last(cls):
		''' Returns the last element in the database.  By default,
			it returns the last element added but if SORT_PARAMETER 
			is defined, it will use this '''

		obj = cls()
		cursor = obj._collection.find().sort(obj._SORT_PARAMETER,pymongo.DESCENDING)

		# check that objects existed
		if cursor.count() > 0:
			return list(cursor)[0]

		return []

	@classmethod
	def search(cls,regex):
		''' Returns all objects in the database that match the 
			given regular expression '''
		pass

	@classmethod
	def deleteAll(cls):
		''' Removes all documents from the database '''
		obj = cls()
		obj._db.drop_collection(obj._COLLECTION_NAME)

	# returns the total number of documents in the database
	@classmethod
	def count(cls):
		''' Returns a count of all objects in the database '''
		return cls()._collection.find().count()
		# return self._collection.find().count()
	#####################################################
	#
	#			Fields
	#
	#####################################################
	_COLLECTION_NAME = ''
	_DB_NAME = ''
	_UPDATE_PARAMETER = ''
	_QUERY_PARAMETERS = ''
	_SORT_PARAMETER = ''
	_OBJECT_CLASS = None

	''' 
		TODO: _MAX_ID should be saved in it's own collection (or somehow
			should persist between sessions)
	'''
	_MAX_ID = 0

	#####################################################
	#
	#			Properties
	#
	#####################################################
	@property
	@abstractmethod
	def _COLLECTION_NAME(self):
		return self._COLLECTION_NAME

	@property
	@abstractmethod
	def _DB_NAME(self):
		return self._DB_NAME

	@property
	@abstractmethod
	def _UPDATE_PARAMETER(self):
		return self._UPDATE_PARAMETER

	@property
	@abstractmethod
	def _QUERY_PARAMETERS(self):
		return self._QUERY_PARAMETERS
	
	@property
	@abstractmethod
	def _SORT_PARAMETER(self):
		return self._SORT_PARAMETER
	
	#####################################################
	#
	#			Methods
	#
	#####################################################
	def __init__(self):
		self._client = MongoClient('mongodb://localhost:27017')
		self._db = self._client[self._DB_NAME]
		self._collection = self._db[self._COLLECTION_NAME]

		self._MAX_ID = self.get_max_id()
		self._MAX_ID += 1
		self.id = self._MAX_ID
	
	def get_max_id(self):
		cursor = self._collection.find().sort('id',pymongo.DESCENDING)
		l = list(cursor)

		if l == []:
			return 0

		max_id = l[0]['id']
		return int(max_id)
	
	def get_properties(self):
		''' Gets the fields that the user wants to store in the databse. '''


		# gets all fields that are not 
		res = inspect.getmembers(self, lambda item : not inspect.isroutine(item))
		res = {a[0]: a[1] for a in res if not((a[0].startswith('__') and a[0].endswith('__')) or 
						a[0].startswith('_') or a[0] == 'objects')}

		return res

	def save(self):
		''' Saves the current object into the database.
			If the object already exists in the database, it updates
			the current object.  Else, it adds the object 
			into the database.
		'''
		properties = self.get_properties()
		self._collection.update_one({'id':properties['id']},
									{'$set':properties},
									upsert=True)
