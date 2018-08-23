import click
from journal import Journal
import re
import datetime

from helpers import get_entry_text, choose_entry

CONTEXT_SETTINGS = dict(help_option_names=['-h','--help'])

from journal import Journal

global journal
journal = Journal()

@click.group(context_settings=CONTEXT_SETTINGS)
def run_command():
	"""\tThis script provides a basic journaling interface.  
	It provides access to storing journal entries and listing all 
	the journal entries."""
	pass

''' Here we have the commands '''
@run_command.command(help='Adds a new journal entry to the journal.')
def add():
	date = datetime.datetime.now()
	entry_text = get_entry_text()

	journal.date = date
	journal.entry = entry_text

	journal.save()

@run_command.command(help='Lists all journal entries.')
@click.option(	'--color','-c',
				help='Enable colorized output.  Only recommended if working in a terminal string literal.',
				is_flag=True,default=False)
def list(color):
	entries = journal.all()
	if entries == []:
		return

	# map the str() function onto the entries list
	tmp = map(str,entries)

	# print results seperated by two newlines
	print('\n\n'.join([item for item in tmp]))

@run_command.command(help='Searches for a valid journal entry.')
@click.option('--regex',
				help='Enable regular expression pattern matching. Default is true.',
				is_flag=True,
				default=True)
def search(regex):
	pattern = input('Enter pattern to search for: ')

	# compile the regex 
	regex = re.compile(pattern)

	matches = journal.match_entries(regex)

	if matches is None:
		return

	results = map(str,matches)

	print('\n\n'.join([item for item in results]))
	

"""
@run_command.command(help='Removes a particular journal entry.')
def delete():
	entries = journal.get_all_entries()
	if entries is None:
		return
	
	entry = choose_entry(entries)

	if entry is None:
		return

	journal.delete_entry(entry.date)
	"""

@run_command.command(help='Shows the last entry in the journal')
def last():
	entry = journal.get_last()
	if entry is not None:
		print(str(entry))

@run_command.command(help='Deletes all journal entries. Cannot be undone.')
def clear():
	journal.deleteAll()

@run_command.command(help='Allows the user to edit a past journal entry.')
@click.option('-c','--choice',help="""Edit the last entry in the journal""",
				is_flag=True,default=True)
def edit(choice):
	entries = journal.all()
	if entries is None:
		return
	
	entry = choose_entry(entries)

	if entry is None:
		return
	
	entry.entry = get_entry_text(entry.entry)

	journal.save()

@run_command.command(help='Shows the total number of entries in the journal.')
def count():
	cursor = journal.count()
	print('Total entries: %d' % cursor)
