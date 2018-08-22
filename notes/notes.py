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


class Notes(Document):
	_DB_NAME =				'cli_apps'
	_COLLECTION_NAME =		'notes'
	_UPDATE_PARAMETER =		''
	_QUERY_PARAMETERS =		''
	_SORT_PARAMETER =		'date'

	_CLASSES = [
		'Anime',
		'Web_dev',
		'Network_Security',
		'CS_Seminar',
		'SC_Toolbox'
	]

	def __init__(self,course=None):
		if course is not None:
			self._COLLECTION_NAME = course + "_notes"

		super().__init__()

	date = datetime.datetime.now() 
	entry = ''
	subject = ''


	def __str__(self):
		print(sys.path)
		tmp_date = self.date.strftime("%B %d, %Y")
		coloredSubject = colored(self.subject,'blue',attrs=['bold'])
		coloredDate = colored(str(tmp_date),'red',attrs=[])
		return coloredSubject + '\n' + coloredDate + "\n" + self.entry
	

