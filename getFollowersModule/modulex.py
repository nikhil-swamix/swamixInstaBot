import os
import random
import json

usepypy=False
if usepypy==True:
	import sys
	if sys.executable.endswith('pypy3.exe'):
		import getpass
		user=getpass.getuser()
		pathlist=[
			f'C:\\Users\\{user}\\AppData\\Local\\Programs\\Python\\Python37',
			f'C:\\Users\\{user}\\AppData\\Local\\Programs\\Python\\Python37\\lib\\site-packages',
			]
		sys.path.extend(pathlist)

# SET DATABASE ------------------
def setload(path,seperator='\n'): return set(fread(path).split(seperator))
def setwrite(path,setDataType): fwrite(path,"\n".join(setDataType))
def setupdate(path,newset):
	diff=newset - setload(path)
	if diff:
		fappend(path,'\n'.join(diff))
# SET DATABASE ------------------
def dictdifference(A,B): return dict(A.items() - B.items())

# FILES SYSTEM-------------------
def fread(path): f=open(path,'r+',encoding='utf-8').read() ;return f
def fwrite(fpath,content): f=open(fpath,"w+",errors="ignore") ;f.write(content)
def fappend(fname,content,suffix='\n',prefix=''): f=open(fname,"a") ;f.write(prefix+content+suffix)
def touch(fpath):
	head=os.path.split(fpath)[0]
	os.makedirs(head,exist_ok=True)
	if not os.path.exists(fpath):
		open(fpath,"w+",errors="ignore").close()
		print('Touched',fpath)

#JSON----------------------------
def jloads(string): return json.loads(string) #dict
def jload(path): 	return json.load(open(path)) #return dict
def jdumps(dictonary,indent=4): return json.dumps(dictonary,indent=indent) #return string
def jdump(dictonary,path): 	return json.dump(dictonary,open(path,"w+"),indent=4) #write to disk
def jdumpline(dictonary,indent=None):return json.dumps(dictonary,indent=indent)
def jdumplines(dictionary,path): [fappend(path,jdumpline({k:dictionary[k]})) for k in dictionary]
def jloadlines(path):	
	jsonlines=open(path,'r').readlines()
	jldict={}
	for w in jsonlines:
		try: jldict.update(jloads(w))
		except: pass
	return jldict

def list_files_timesorted(folder):
	return [folder+x for x in os.listdir(folder)].sort(key=os.path.getmtime)

#TIMESTAMPERS---------------------
def datetime(filesafe=1):
	from datetime import datetime
	template='%Y%m%dT%H%M%S' if filesafe else '%Y-%m-%dT%H:%M:%S'
	return datetime.today().strftime(template)

def date():
	return datetime().split('T')[0]

def now():
	import time
	return int(time.time())

#RANDOMIZERS ---------------------
def shuffle(L): return [pickrandom(L) for x in range(len(L))]
def randindex(L): return random.randrange(len(L)) # get random index
def poprandom(L):
	i = randindex(L) 
	L[i], L[-1] = L[-1], L[i] # swap with the last element
	return L.pop() # pop last element O(1)


#GENERATORS___________________________________
asciirange=('0', '1', '2', '3', '4', '5', '6', '7', '8', '9',  \
'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', \
'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', \
'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', \
'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', \
'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z')
def randomstring(length):
	lenascii=len(asciirange)
	r=[str(asciirange[random.randrange(lenascii)]) for x in range(length) ]
	return ''.join(r)

def hash(string): import hashlib; return hashlib.md5(string.encode('utf-8')).hexdigest()

#AUTO_PIP______________________________________
def auto_pip(modulesList,mode='install'):
	'''
		+DOC: 
			automatically Install Pip Packages With Missing Module && upgrades pip if its old, 
		+USAGE: 
			auto_pip('mode',[modules,...]) #where mode can be {install,uninstall,download} and modules is
			auto_pip('install',['pytorch','numpy','etc...']) 
		+NOTES: downloading can be useful if want to install later 
		from local source and avoid network cost.
	'''
	modulesList=[modulesList] if isinstance(modulesList,str) else modulesList
	import subprocess as sp
	proc=sp.run('pip list',stdout=sp.PIPE,stderr=sp.PIPE,text=1)
	if 'You should consider upgrading' in proc.stderr:
		upgradeCommand=proc.stderr.split('\'')
		sp.run(upgradeCommand[1])

	pipInstallSignal,pipUninstallSignal= 0,0 #declare signals as 0,
	satisfied={x:(x.lower() in proc.stdout.lower()) for x in modulesList} 
	for k,v in satisfied.items():
		print(k+'\t:preinstalled') if v else print(k,'is missing',end=' =|= ')
		if v==False: pipInstallSignal=1  
		if v==True: pipUninstallSignal=1 #NAND Condition if true then start uninstalling
	
	if mode=='download':
		proc=sp.run(f'pip download {" ".join(modulesList)} ' ,stdout=sp.PIPE	,shell=0)
		output=proc.stdout.read().decode('ascii').split('\n')
		print([x for x in output if 'Successfully' in x][0])
		proc.kill()
			
	if mode=='install': 
		if pipInstallSignal==True: 
			proc=sp.run('pip install {} -U'.format(" ".join(modulesList)),text=True,shell=1)
		else: print(f'{modulesList} were already installed'); return 1 

	if mode=='uninstall': 
		if pipUninstallSignal==True: 
			proc=sp.run('pip uninstall -y {}'.format(" ".join(modulesList)),text=True,shell=0)
		else: print(f'\n{modulesList} were already uninstalled'); return 1

	if proc.returncode==0:
		print('auto_pip Run Success')
		return proc.returncode

#SIMPLE-DB_________________________________
def hash_db(hashkey,*hashvalue,dirname='./LOCAL_DATABASE/'):
	''' 
		if : an index(hashkey) is given then check is file exists and open and return a dict{}
		else : if second argument (hashvalue[]) is given then create a dict
	'''
	itempath=dirname+hashkey
	if hashvalue:#write inputted value to memory
		fwrite(itempath,jdumps(hashvalue[0]))
	return jload(itempath)

#THREADING__________________________________
class Parallelizer:
	def tpoolmap(fn,*iters,threads=16):
		from concurrent.futures import ThreadPoolExecutor
		print(f'__________ThreadPool Made with {threads} threads')
		POOL=ThreadPoolExecutor(threads)
		result=POOL.map(fn,*iters)
		return result

#WEBFN______________________________________

def make_session_pool(count=1): return [requests.Session() for x in range(count)]

def get_page(url,headers={}): #return a page req object and retrive text later
	import requests
	UserAgent={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:86.0) Gecko/20100101 Firefox/86.0'}
	# UserAgent={'User-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_3 like Mac OS X) AppleWebKit/603.3.8 (KHTML, like Gecko) Mobile/14G60 Instagram 12.0.0.16.90 (iPhone9,4; iOS 10_3_3; en_US; en-US; scale=2.61; gamut=wide; 1080x1920)'}
	headers.update(UserAgent)
	req=requests.get(url,headers=headers)
	if not req: #send headers only when invalid response
		req = requests.get(url,headers=headers)
	return req

def make_soup(markup): 
	from bs4 import BeautifulSoup as soup
	return soup(markup,'html.parser')

def get_page_soup(url,headers={}): return make_soup(get_page(url,headers=headers).text)

def make_selenium_driver(headless=True,strategy='normal',timeout=5):
	from selenium import webdriver as wd
	opts = wd.firefox.options.Options();
	opts.page_load_strategy = strategy
	if headless: 
		opts.headless = True
	# opts.add_argument("--headless")
	driver=wd.Firefox(options=opts)
	driver.set_page_load_timeout(timeout)
	driver.implicitly_wait(10)	
	return driver 

def get_page_selenium(driver,url,new_tab=0):
	try:
		if new_tab:
			driver.execute_script("window.open('{}', '_blank')".format(url))

		driver.get(url)
		return driver.page_source
	except Exception as e:	
		print((e))

def parse_header(firefoxAllHeaders):
	serializedHeaders=list((firefoxAllHeaders).values())[0]['headers']
	return { k:v for k,v in [x.values() for x in serializedHeaders] }

def parse_cookie():
	...

def wlan_ip():
    import subprocess
    result=subprocess.run('ipconfig',stdout=subprocess.PIPE,text=True).stdout.lower()
    scan=0
    for i in result.split('\n'):
        if 'wireless' in i:
            scan=1
        if scan:
            if 'ipv4' in i:
                print (i.split(':')[1].strip())

# MONITORS _____________________________________
def timeit(fn,*args,times=1000):
	import time
	ts=time.time()
	print(f'Running: {fn.__name__} | {times} Times')
	for x in range(times):
		fn(*args)
	tdelta=time.time() - ts
	print(f"TDelta:{(tdelta)*1000}ms | avgCallTime: {(tdelta/times)*1000}ms")

class Tests:
	def testWebServerStress():
		def reqfn():
			d=requests.get(url2)
			print('fetch success',d.text)
		url1='http://swamix.com/'
		url2='http://swamix.com/api/news/tech'
		Parallelizer.tpoolexec(reqfn,threadCount=100)

if __name__ == '__main__':
	...
	print(randomstring(100))
	print(hash('_nikhil_swami_'))

	# print(get_page('https://www.newstatesman.com/the-age-of-fitness-jurgen-martschukat-review?utm_source=pocket-newtab-intl-en').text)

		
	# URL='https://swamix.com/medium/https://timesofindia.indiatimes.com/india/why-was-rasputin-dancing-in-kerala/articleshow/82054212.cms'
	# URL='https://docs.python-requests.org/en/v0.8-0/user/quickstart/'
	# p=get_page(URL,headers={'Accept-Encoding':'gzip'}).headers
	# print(p)