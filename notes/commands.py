import click
from notes import Notes
import re
import datetime

from helpers import get_entry_text, choose_entry

CONTEXT_SETTINGS = dict(help_option_names=['-h','--help'])

from notes import Notes

global notes
notes = Notes()

@click.group(context_settings=CONTEXT_SETTINGS)
def run_command():
	"""\tThis script provides a basic notesing interface.  
	It provides access to storing notes entries and listing all 
	the notes entries."""
	pass

def chooseClass(classes):
	i = 1
	for subject in classes:
		print('%d: %s' % (i, subject))
		i += 1
	choice = input('Choose subject: ')
	
	choice = int(choice.strip())

	if choice - 1 not in range(len(classes)):
		return None
	
	return classes[choice - 1]


''' Here we have the commands '''
@run_command.command(help='Adds a new notes entry to the notes.')
def add():
	date = datetime.datetime.now()
	subject = chooseClass(notes._CLASSES)

	if subject is None:
		exit()

	entry_text = get_entry_text()

	notes.date = date
	notes.entry = entry_text
	notes.subject = subject

	notes.save()

@run_command.command(help='Lists all notes entries.')
@click.option(	'--color','-c',
				help='Enable colorized output.  Only recommended if working in a terminal string literal.',
				is_flag=True,default=False)
def list(color):
	entries = notes.all()
	# entries = notes.get_all_entries()
	if entries == []:
		exit()

	# map the str() function onto the entries list
	tmp = map(str,entries)

	# print results seperated by two newlines
	print('\n\n'.join([item for item in tmp]))

@run_command.command(help='Searches for a valid notes entry.')
@click.option('--regex',
				help='Enable regular expression pattern matching. Default is true.',
				is_flag=True,
				default=True)
def search(regex):
	pattern = input('Enter pattern to search for: ')

	# compile the regex 
	regex = re.compile(pattern)

	matches = notes.match_entries(regex)

	if matches is None:
		return

	results = map(str,matches)

	print('\n\n'.join([item for item in results]))
	

"""
@run_command.command(help='Removes a particular notes entry.')
def delete():
	entries = notes.get_all_entries()
	if entries is None:
		return
	
	entry = choose_entry(entries)

	if entry is None:
		return

	notes.delete_entry(entry.date)
	"""

@run_command.command(help='Shows the last entry in the notes')
def last():
	entry = notes.get_last()
	if entry is not None:
		print(str(entry))

@run_command.command(help='Deletes all notes entries. Cannot be undone.')
def clear():
	notes.deleteAll()

@run_command.command(help='Allows the user to edit a past notes entry.')
@click.option('-c','--choice',help="""Edit the last entry in the notes""",
				is_flag=True,default=True)
def edit(choice):
	entries = notes.all()
	if entries is None:
		return
	
	entry = choose_entry(entries)

	if entry is None:
		return
	
	tmp_entry = get_entry_text(entry.entry)
	entry.entry = tmp_entry
	print('entry is', tmp_entry)

	entry.save()

@run_command.command(help='Shows the total number of entries in the notes.')
def count():
	cursor = notes.count()
	print('Total entries: %d' % cursor)
