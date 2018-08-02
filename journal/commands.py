import click
from journal import Journal
import re

CONTEXT_SETTINGS = dict(help_option_names=['-h','--help'])

global journal
journal = Journal()

from journal import Journal2

@click.group(context_settings=CONTEXT_SETTINGS)
def run_command():
	"""\tThis script provides a basic journaling interface.  
	It provides access to storing journal entries and listing all 
	the journal entries."""
	pass

''' Here we have the commands '''
@run_command.command(help='Adds a new journal entry to the journal.')
def add():
	journal.addEntry()
	journal.save()

@run_command.command(help='Lists all journal entries.')
@click.option(	'--color','-c',
				help='Enable colorized output.  Only recommended if working in a terminal string literal.',
				is_flag=True,default=False)
def list(color):
	journal = Journal2()
	entries = journal.get_all_entries()
	if entries is None:
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
	matches = journal.search(re.compile(pattern))
	for item in matches:
		print(item)
	

@run_command.command(help='Removes a particular journal entry.')
def delete():
	journal.deleteEntry()
	journal.save()

@run_command.command(help='Shows the last entry in the journal')
def last():
	journal = Journal2()
	entry = journal.get_last_entry()
	if entry is not None:
		print(str(entry))

@run_command.command(help='Deletes all journal entries. Cannot be undone.')
def clear():
	journal = Journal2()
	journal.delete_all_entries()

@run_command.command(help='Allows the user to edit a past journal entry.')
@click.option('-c','--choice',help="""Edit the last entry in the journal""",
				is_flag=True,default=True)
def edit(choice):
	journal.editEntry(choice)
	journal.save()
