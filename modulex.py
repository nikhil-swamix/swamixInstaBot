#last fetched on 2022-08-09 00:12:56.517162
# V2.0
##     ##  #######  ########  ##     ## ##       ######## ##     ##
###   ### ##     ## ##     ## ##     ## ##       ##        ##   ##
#### #### ##     ## ##     ## ##     ## ##       ##         ## ##
## ### ## ##     ## ##     ## ##     ## ##       ######      ###
##     ## ##     ## ##     ## ##     ## ##       ##         ## ##
##     ## ##     ## ##     ## ##     ## ##       ##        ##   ##
##     ##  #######  ########   #######  ######## ######## ##     ##
# ▀█████████▄  ▄██   ▄
#   ███    ███ ███   ██▄
#   ███    ███ ███▄▄▄███
# _ ▄███▄▄▄██▀  ▀▀▀▀▀▀███
# ▀▀███▀▀▀██▄  ▄██   ███
#   ███    ██▄ ███   ███
#   ███    ███ ███   ███
# ▄█████████▀   ▀█████▀

# ███╗   ██╗██╗██╗  ██╗██╗  ██╗██╗██╗
# ████╗  ██║██║██║ ██╔╝██║  ██║██║██║
# ██╔██╗ ██║██║█████╔╝ ███████║██║██║
# ██║╚██╗██║██║██╔═██╗ ██╔══██║██║██║
# ██║ ╚████║██║██║  ██╗██║  ██║██║███████╗
# ╚═╝  ╚═══╝╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝╚══════╝
# ███████╗██╗    ██╗ █████╗ ███╗   ███╗██╗
# ██╔════╝██║    ██║██╔══██╗████╗ ████║██║
# ███████╗██║ █╗ ██║███████║██╔████╔██║██║
# ╚════██║██║███╗██║██╔══██║██║╚██╔╝██║██║
# ███████║╚███╔███╔╝██║  ██║██║ ╚═╝ ██║██║
# ╚══════╝ ╚══╝╚══╝ ╚═╝  ╚═╝╚═╝     ╚═╝╚═╝


import os
import time
import random
import json


import sys

# SET DATABASE ------------------


def setload(path, seperator="\n"):
	rset = set(fread(path).split(seperator))
	rset.remove("") if "" in rset else ""
	return rset


def setwrite(path, setDataType):
	fwrite(path, "\n".join(setDataType) + "\n")


def setupdate(path, newset):
	diff = newset - setload(path)
	if diff:
		fappend(path, "\n".join(diff))


# SET DATABASE ------------------
def dictdifference(A, B):
	return dict(A.items() - B.items())


# FILES SYSTEM-------------------
def fread(path):
	f = open(path, "r+", encoding="utf-8").read()
	return f


def fwrite(fpath, content):
	f = open(fpath, "w+", encoding="utf-8", errors="ignore")
	f.write(content)


def fappend(fname, content, suffix="\n"):
	f = open(fname, "a")
	f.write(content + suffix)


def touch(fpath, data=""):
	try:
		os.makedirs(os.path.split(fpath)[0], exist_ok=True)
	except:  # noqa: E722
		pass
	if not os.path.exists(fpath):
		fwrite(fpath, data)
		print("Touched", fpath)


def fgetlastmod(path):
	'''
	Get Last modified time of a file
	'''
	return time.time() - os.path.getmtime(path)


def fincrement(cname, lock=None):
	'''
	uses a file as incrementer, slow, use in
	rare cases where you would need persistance storage.
	Uses lock to prevent I/O race condition.
	lock is derived from threading module.
	'''
	if lock:
		with lock.acquire() as l:  # noqa: E741
			c = int(fread(cname))
			c += 1
			fwrite(cname, str(c))
			l.release()
	else:
		print("please use lock")

# JSON----------------------------


def jloads(string):
	return json.loads(string)  # dict


def jload(path):
	return json.load(open(path,encoding='utf-8',errors='ignore'))  # return dict


def jdumps(dictonary, indent=4):
	return json.dumps(dictonary, indent=indent)  # return string


def jdump(dictonary, path):
	return json.dump(dictonary, open(path, "w+"), indent="\t")  # write to disk


def jdumpline(dictonary, indent=None):
	return json.dumps(dictonary, indent=indent)


def jdumplines(dictionary, path):
	[fappend(path, jdumpline({k: dictionary[k]})) for k in dictionary]


def jloadlines(path):
	jsonlines = open(path, "r").readlines()
	jldict = {}
	for w in jsonlines:
		try:
			jldict.update(jloads(w))
		except Exception:
			pass
	return jldict


def list_files_timesorted(folder):
	return [folder + x for x in os.listdir(folder)].sort(key=os.path.getmtime)


# TIMESTAMPERS---------------------


def datetime(filesafe=1):
	from datetime import datetime
	template = "%Y%m%dT%H%M%S" if filesafe else "%Y-%m-%dT%H:%M:%S"
	return datetime.today().strftime(template)


def date():
	return datetime().split("T")[0]


def now():
	import time
	return int(time.time())


# RANDOMIZERS ---------------------


def shuffle(L):
	return [poprandom(L) for x in range(len(L))]


def randindex(L):
	return random.randrange(len(L))  # get random index


def poprandom(L):
	i = randindex(L)
	L[i], L[-1] = L[-1], L[i]  # swap with the last element
	return L.pop()  # pop last element O(1)


# GENERATORS___________________________________
asciirange = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


def randomstring(length):
	lenascii = len(asciirange)
	r = [str(asciirange[random.randrange(lenascii)]) for x in range(length)]
	return "".join(r)


def hash(string):
	import hashlib

	return hashlib.md5(string.encode("utf-8")).hexdigest()


# REQUIRE: THE DEPENDENCY MANAGER____________________
def require(modules_list: list[str]):
	if type(modules_list) is list:
		pass
	else:
		modules_list = [modules_list]

	for m in modules_list:
		try:
			exec(f'import {m}')

		except Exception as e:
			print(e)
			os.system(f"pip install {m}")


# SIMPLE-DB_________________________________
def hash_db(hashkey, *hashvalue, dirname="./LOCAL_DATABASE/"):
	"""
	DESC:
		creates a folder , and stores individual hashes as files.
		if: an index(hashkey) is given then check is file exists and open and return a dict{}
		else: if second argument (hashvalue[]) is given then create a dict
	"""
	itempath = dirname + hashkey
	if hashvalue:  # write inputted value to memory
		fwrite(itempath, jdumps(hashvalue[0]))
	return jload(itempath)


# THREADING__________________________________
MAX_THREADS = 128


def apply_async(*args):
	global POOL
	from concurrent.futures import ThreadPoolExecutor

	try:
		result = POOL.submit(
			*args,
			)
		return result
	except Exception:
		POOL = ThreadPoolExecutor(MAX_THREADS)
		result = POOL.submit(
			*args,
			)
		return result


# WEBFN______________________________________
def get_random_proxy():
	import re

	fname = "proxylist.set"
	sourceurl = "https://free-proxy-list.net/"
	cacheTime: "seconds" = 30

	if os.path.exists(fname):
		tdelta = time.time() - os.path.getmtime(fname)
		if tdelta >= cacheTime:
			pass
		else:
			print(f"LOG: using preexisting proxyDB: created {tdelta}s ago ")
			return setload(fname).pop()

	page = get_page(sourceurl)
	iplist = re.findall(r"[\d]+\.[\d]+\.[\d]+\.[\d]+:[\d]+", page.text)
	proxylist = {"http://" + x for x in iplist}
	setwrite(fname, proxylist)
	print("LOG: refreshed proxy list")
	return proxylist.pop()


def make_session_pool(count=1):
	return [requests.Session() for x in range(count)]


UserAgent = {
	"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0"
}


def get_page(url, headers={}):  # return a page req object and retrive text later
	import requests

	# headers.update(UserAgent)
	req = requests.get(url, headers=headers)
	return req


def post_page(
    url,
    data,
    headers={},
):
	import requests

	r = requests.post(url, json=data, headers=headers)
	if not r:
		r = requests.post(url, data=data, headers=headers)

	return r


def make_soup(markup):
	from bs4 import BeautifulSoup as soup

	try:
		return soup(markup, "lxml")
	except Exception as e:
		return soup(markup, "html.parser")


def get_page_soup(url, headers={}):
	return make_soup(get_page(url, headers=headers).text)


def make_selenium_driver(headless=False, strategy="eager", timeout=10):
	from selenium import webdriver as wd

	opts = wd.firefox.options.Options()
	opts.page_load_strategy = strategy
	if headless:
		opts.headless = True
	# opts.add_argument("--headless")
	driver = wd.Firefox(options=opts)
	driver.set_page_load_timeout(timeout)
	driver.implicitly_wait(10)
	return driver


def get_page_selenium(
	driver,
	url,
	new_tab=0,
	delay=2,
	waitcondition=lambda: True,
	waitcondition_polling=0.2,
	waitcondition_retries=10,
):
	try:
		if new_tab:
			driver.execute_script("window.open('{}', '_blank')".format(url))
		driver.get(url)

		while waitcondition() is False:
			if retry >= waitcondition_retries:
				break
			time.sleep(waitcondition_polling)

		return driver.page_source
	except Exception as e:
		print(repr(e))


def parse_header(*firefoxAllHeaders, file=""):
	if firefoxAllHeaders:
		rawheader = firefoxAllHeaders[0]
	if file:
		rawheader = jload(file)
	serializedHeaders = list((rawheader).values())[0]["headers"]
	# print(serializedHeaders)
	return {k: v for k, v in [x.values() for x in serializedHeaders]}


def parse_raw_headers(fpath, log=0):
	headers = {}
	for x in open(fpath).read().split('\n'):
		d = dict([[y.strip() for y in x.split(':', 1)]])
		headers.update(d)
		if log: 
			print(d) 
	return headers


def make_cookie(req):
	return ";".join([f"{k}={v}" for k, v in req.cookies.items()])


def auto_encoder(d):
	'''encode dict to url get params'''
	string = "&".join([f"{k}={urllib.parse.quote_plus(str(v))}" for k, v in d.items()])
	return string


def wlan_ip():
	import subprocess

	result = subprocess.run(
		"ipconfig", stdout=subprocess.PIPE, text=True
		).stdout.lower()
	scan = 0
	for i in result.split("\n"):
		if "wireless" in i:
			scan = 1
		if scan:
			if "ipv4" in i:
				print(i.split(":")[1].strip())


# Benchmarking _________________
def timeit(fn, *args, times=1000, verbose=False):
	import time

	ts = time.time()
	print(f"LOG: run {fn.__name__} X {times} Times") if verbose else None
	for x in range(times):
		fnoutput = fn(*args)
	tdelta = time.time() - ts
	print(f"LOG: Ttotal: {(tdelta)*1000}ms | time/call: {(tdelta/times)*1000}ms") if verbose else None
	print(f"LOG: output == ", fnoutput) if verbose else None
	return tdelta


class Tests:
	def testWebServerStress():
		def reqfn():
			d = requests.get(url2)
			print("fetch success", d.text)

		# url1 = "http://swamix.com/"
		url2 = "http://swamix.com/api/news/tech"
		Parallelizer.tpoolexec(reqfn, threadCount=100)  # noqa: F821


def i_want_to_release_this_version_on_github():
	os.system(f"git commit -m \"force committed on \"")
	os.system("git push -f")

#                  _                       _
#                 (_)                     | |
#  _ __ ___   __ _ _ _ __     ___ ___   __| | ___
# | '_ ` _ \ / _` | | '_ \   / __/ _ \ / _` |/ _ \
# | | | | | | (_| | | | | | | (_| (_) | (_| |  __/
# |_| |_| |_|\__,_|_|_| |_|  \___\___/ \__,_|\___|
# _________________________________________________


if __name__ == "__main__":
	print(randomstring(100))
	# require(['numpy', 'pandas', 'bs4'])


# html body div#root div.a.b.c div.s article.meteredContent div section.de.df.dg.dh.di
