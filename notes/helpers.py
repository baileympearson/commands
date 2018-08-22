
import sys, tempfile, os
import subprocess
from termcolor import colored



def get_entry_text(entry = ''):
	EDITOR = os.environ.get('EDITOR') if os.environ.get('EDITOR') else 'vim'

	entry = bytes(entry,'utf-8')
	with tempfile.NamedTemporaryFile(suffix=".tmp") as tf:
		tf.write(entry)
		tf.flush()
		subprocess.call([EDITOR,tf.name])

		tf.seek(0)
		edited_message = tf.read().decode('utf-8')
	return edited_message


def choose_entry(entries):
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
