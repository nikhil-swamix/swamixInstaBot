import sys
import os
from datetime import datetime

try:
	import requests
except Exception as e:
	os.system('pip install requests')

VERSION_LOCK = 1


def progressive_import():
	global mx
	success = 0
	importlevel = "./"
	try:
		import modulex as mx
		# print("mx importlevel", importlevel)
	except Exception:
		for i in range(4):
			importlevel += "../"
			if not success:
				try:
					sys.path.append(importlevel)
					from modulex import modulex as mx
					success = 1
					print("LOG: mx imported level", importlevel)
				except Exception as e:
					print(e)


def fetch_latest_copy():
	url = 'https://raw.githubusercontent.com/BinarySwami-10/modulex/master/modulex.py'
	# print((mx.get_page('https://raw.githubusercontent.com/BinarySwami-10/modulex/master/modulex.py').text))
	if not os.path.exists('modulex.py'):
		pagedata = requests.get(url).text
		print('page fetched, now writing')
		open('modulex.py', '+w', encoding="utf-8").write(f"#last fetched on {datetime.now()}\n" + pagedata,)
	else:
		print('Modulex already present')


if os.path.exists('.git'):
	fetch_latest_copy()
	progressive_import()
else:
	progressive_import()
