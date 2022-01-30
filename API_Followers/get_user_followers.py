from mxproxy import mx
import time
import os
import re
import requests


def get_userid(username):
	id = mx.get_page(f'https://www.instagram.com/{username}/?__a=1').json()['graphql']['user']['id']
	print({username: id})
	return id


def get_end_cursor(dictobj):
	return dictobj['data']['user']['edge_followed_by']['page_info'].get('end_cursor')


def get_followers_list(userid='', headers=''):
	'''
	ABOUT (apiurlprefix): 
		please note that variable (apiurlprefix) is url of my account,
		it may slightly differ for you,	to identify correct url, go to chrome, open inspect
		element, then go to	network tab, and open your instagram account and open followers
		tab, now the app (aka your browser) makes a request to server with your client api
		parameters. so as soon as you open your followers list, then check the latest request
		in network tab, that is the url you are looking for my friend, now check its response,
		it will be a JSON derulo. all stuff i have done here is parsing the json and calculating
		logical difference of followers aka tracking based on timestamps.
	About (userid):
		do not worry about userid, it can be fetched/resolved with
		'get_userid' function which i wrote above,	in the if main block below,
		just change the variable for example userid='_nikhil_swami_', rest assured handled. 
	ABOUT (headers):
		headers are sent with request module as request.get(url,headers={'apple':'ball'}), its basically,
		the method of sending mini data with each request, here our mini data is cookie , it helps the 
		server to identify you are you, like a id-card. so please get your cookie from the browser via
		Browser->inspect_element->network_tab->Request_Headers->Cookie.
	'''
	if not userid:
		print('Please Specify UserID userid=123321232...')
		return
	if not headers:
		print('Use headers from your browser after you sign in from your account, to imitate get followers request with cookies')
		return

	followers_list = []
	apiurlprefix = f'https://i.instagram.com/api/v1/friendships/{userid}/followers/?count=120'
	apiresponse = requests.get(apiurlprefix, headers=headers).json()

	break_signal = 0
	while not break_signal:
		nextCursor = apiresponse.get('next_max_id', '')
		nextUrl = f'{apiurlprefix}&max_id={nextCursor}'
		apiresponse = requests.get(nextUrl, headers=headers).json()
		followers_list.extend([u['username'] for u in apiresponse['users']])
		print("CURSOR =>", nextCursor) if nextCursor else None
		if not nextCursor:  # when=>GraphQL exhaust next node
			print("CURSOR => NONE! QUERY FINISHED ",)
			break_signal = 1
	return followers_list


def calculate_difference(follower_at_t0, follower_at_t1):
	'''need to implement with edge cases,
	f1=open followers list at previous timestamp
	f2=open followers list at current timestamp
	#since sets use '-' for difference calculation 
	return set(f1) - set(f2) 
	'''
	t0 = mx.jload(follower_at_t0)
	t1 = mx.jload(follower_at_t1)

	print("a-b=", set(t0)-set(t1))
	print("b-a=", set(t1)-set(t0))
	return set(t0)-set(t1)


if __name__ == '__main__':
	FETCH_MODE = 1
	CALCULATE_MODE = 0
	user = '_nikhil_swami_'  # user='kruz__022'# user='manasa._.sharma'
	# userid=get_userid(user)
	userid = 2237911879
	if FETCH_MODE:
		try:
			'''
				METHOD1: copy all headers from browser inspector->network->request headers.
				and paste them in ./Accounts/{your_username}/headers.json.
				do not share these headers with anyone!
			'''
			viewer_headers = mx.parse_header(mx.jload('./Accounts/_nikhil_swami_/headers.json'))
			followers_list = get_followers_list(
				userid=userid, headers=viewer_headers)  # FETCH DATA
			# print(followers_list)
		except Exception as e:
			'''
				METHOD2: Mostly works, as mentioned in method1, just use the cookie instead
				the below cookie is corrupted for security reasons.
			'''
			viewer_cookie = {'Cookie': 'ig_did=BFD81740-8321-49E7-BF95-904033F91D51; ig_nrcb=1; mid=Yd3dcAALAAEBfjcVUUwJbjQ30nf8; csrftoken=INEQfVli9mrfxV39RhKX12XFP9aMQg11; sessionid=2237911879:VXLBed0RmxtxEx:9; ds_user_id=2237911879; shbid="2658\0542237911879\0541675080632:01f7b0a6b660464cf3327041788777c35972ade66e96becc5d49833903f3d31975dcb871"; shbts="1643544632\0542237911879\0541675080632:01f7d3f6e9a3689625ee93b083285fa1918ff451bc862e9265bd437887c6cc4c3257c770"; rur="NAO\0542237911879\0541675081307:01f78a2a3dcee5bd8447b78da9426b4ff207356d742e16930e7c853320d315e99bb4d737"'}
			followers_list = get_followers_list(userid=userid, headers=viewer_cookie)  # FETCH DATA
			raise e

		mx.touch(f'./Data/{user}/')
		write_to_disk = mx.jdump(followers_list, f"./Data/{user}/{user}@{mx.datetime()}")
		mylist = [f'{x:20}' for x in followers_list]
		print('\\'.join(mylist))

	if CALCULATE_MODE:
		print('these users have unfollowed')
		datafolder = f'./Data/{user}/'
		timeline = [datafolder+x for x in os.listdir(datafolder) if re.match(fr'{user}@[\d]', x)]
		# print(timeline)
		calculate_difference(timeline[-1], timeline[-2])

	#
	# string='_nikhil_swami_@20210523T220136'
	# print()
	# url='https://i.instagram.com/api/v1/users/2280322955/info/'
	# p=mx.get_page(url,headers=headers).text
	# print(p)
	# attack_later=['suryagr_']#broadcast ashwant friend filth
