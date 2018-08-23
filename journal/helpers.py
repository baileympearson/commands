
import sys, tempfile, os
import subprocess
from termcolor import colored


def get_entry_text(entry = ''):
	''' Helper function used to get the body of the entries '''

	# get the default editor based on user preferences
	EDITOR = os.environ.get('EDITOR') if os.environ.get('EDITOR') else 'vim'

	# entry needs to be a bytes object
	entry = bytes(entry,'utf-8')

	# get the actual body text
	with tempfile.NamedTemporaryFile(suffix=".tmp") as tf:
		# write into the file
		tf.write(entry)
		tf.flush()

		# actually open the editor
		subprocess.call([EDITOR,tf.name])

		# get the entry text from the temp file
		tf.seek(0)
		edited_message = tf.read().decode('utf-8')
	return edited_message


def choose_entry(entries):
	''' Helper function to allow the user to choose
		an entry from a list of entries '''

	i = 1
	for entry in entries:
		s = str(i) + '. '
		tmp_date = entry.date.strftime("%B %d, %Y")
		s += colored(str(tmp_date),'red',attrs=[])
		print(s)
		i += 1
	
	choice = int(input("Choose entry: ").strip())
	if choice - 1 not in range(len(entries)):
		return None

	return entries[choice-1]
