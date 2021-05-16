from mxproxy import mx
import time

def get_userid(username):
	id=mx.get_page(f'https://www.instagram.com/{username}/?__a=1').json()['graphql']['user']['id']
	print({username:id})
	return id

def get_end_cursor(dictobj):
	return dictobj['data']['user']['edge_followed_by']['page_info'].get('end_cursor')

def get_followers_list(userid='',headers=''):
	if not userid:
		print('Please Specify UserID userid=123321232 ...')
		return
	if not headers:
		print('Use headers from your browser after you sign in from your account, to imitate get followers request with cookies')
		return

	apiurlprefix='https://www.instagram.com/graphql/query/?query_hash=5aefa9893005572d237da5068082d8d5'
	variables={"id":userid,"include_reel":True,"fetch_mutual":True,"first":100,"after":None}
	fetch_url=f'{apiurlprefix}&variables={mx.jdumps(variables)}'
	followers_list=[]
	break_signal=0
	while not break_signal:
		pagedict=mx.get_page(fetch_url,headers=headers).json()
		variables.update({"after":get_end_cursor(pagedict)})
		fetch_url=f'{apiurlprefix}&variables={mx.jdumps(variables)}'
		fetched_followers=[x['node']['username'] for x in pagedict['data']['user']['edge_followed_by']['edges']]
		followers_list.extend(fetched_followers)
		print("CURSOR =>",variables['after'])
		if not variables['after']: #when=>GraphQL exhaust next node
			break_signal=1
	return followers_list

def calculate_difference(follower_at_t0,follower_at_t1):
	'''need to implement with edge cases,
	f1=open followers list at previous timestamp
	f2=open followers list at current timestamp
	#since sets use '-' for difference calculation 
	return set(f1) - set(f2) 
	'''
	r=set(mx.jload(follower_at_t0))-set(mx.jload(follower_at_t1))
	print(r)
	return r

if __name__ == '__main__':
	FETCH_MODE=1
	CALCULATE_MODE=0

	if FETCH_MODE:
		userid=get_userid(user:='_nikhil_swami_')
		try:
			'''viewer headers are all the headers of request to perfectly imitate like browser
			since its sensitive data,sorry i cant put mine here. neither you should give to anyone.
			websearch: request library header, to understand more'''
			viewer_headers = mx.parse_header(mx.jload('./Accounts/_nikhil_swami_/headers.json'))
			followers_list=get_followers_list(userid=userid,headers=viewer_headers) #FETCH DATA
		except:
			'''GET This cookie from browser inspect element (google it) , 
			i put wrong cookie here so it will not work, may work if the target account is public,
			partly imitates browser note:cookie of your account allows 
			you to see only the followers of your acc and the people you follow(incl private)
			provided cookie is a dummy cookie, please get new one from browser, it will almost look likethis dummy'''
			viewer_cookie={'Cookie':'mid=YHDvlwALAAH4BiG2WwETlfSomHUD; ig_did=81C89A5B-5478-41A0-8A1A-95481F38BB05; ig_nrcb=1; sessionid=2237d911879%3A4KZ1W25kr7DNiB%3A25; shbid=2658; shbts=1621143238.6504378; fbm_124024574287414=base_domain=.instagram.com; rur=FTW; fbsr_124024574287414=7u1R4V8VkZ_ZR6d7L6fd_WPOIZR1IsAutbczF_lqKNQ.eyJ1c2VyX2lkIjoiMTAwMDAyNDM1NTEwNjQ3IiwiY29kZSI6IkFRQllXam1qZERST1pycnF5Z3JrcEVaT0hyek9waGY2SUZ0VVpIdzhMbWQ3Z3hZQjZXeVNvR3RUUGRXWVVscXdCN1NDS2Nwb0ZpbjFFRFBiWktqU085Q0lrRVREZk1VNDdfbzVyMHFMYkI1NUdqd0FIOTZUNThNNTFoMGlPNUFFWWh4TGo2b1drVkVjM2N3TmJFUVUzSmQteVdwSUJwRVpmaldFYllKWFladGgwQUI5ZG5naDU1cXhxdVdKMXlYTFhiSHVwOHdDRFcxN2lzSGdXLWo0UU9PZm84NzQ1NGpHWHNoY2JGUlFtM1N5THA0eGlYVE44VFNhTUU0NVM0c3FwbURvMFpHdnVlb2pKUTQyT3VmcFZ2MGN3aHRVLWhDYzlmZEF1ZEhiblBlWWY0OEdQbXVNbnpaN2MyODdhekRSSFZSbTRIb2g1eFVDdHliUFNNTGlHSUJ2Iiwib2F1dGhfdG9rZW4iOiJFQUFCd3pMaXhuallCQUZwWGxqcFdEeDBmeExLU2FYcXVqd2tuU2hNZGhYWGtNTDFWclpCaUFTTXozSElZczFzNjJ0YWg0aFpDbVJXeHRoWkJBdUF3Sng0ZG5IUnV3Rmo5VDh5Z0tva1pBNzg1bTE2cmZMeEN4cnpVSk9ZQU0yR2tsUjJLbEFoUjRQYzFtYjltUXBCdnRnczlRbnNUdWVjWkNVWkNzZmNuN2FHbGoyOHE1QXdOdGciLCJhbGdvcml0aG0iOiJITUFDLVNIQTI1NiIsImlzc3VlZF9hdCI6MTYyMDcyNjY3OX0; fbsr_124024574287414=7u1R4V8VkZ_ZR6d7L6fd_WPOIZR1IsAutbczF_lqKNQ.eyJ1c2VyX2lkIjoiMTAwMDAyNDM1NTEwNjQ3IiwiY29kZSI6IkFRQllXam1qZERST1pycnF5Z3JrcEVaT0hyek9waGY2SUZ0VVpIdzhMbWQ3Z3hZQjZXeVNvR3RUUGRXWVVscXdCN1NDS2Nwb0ZpbjFFRFBiWktqU085Q0lrRVREZk1VNDdfbzVyMHFMYkI1NUdqd0FIOTZUNThNNTFoMGlPNUFFWWh4TGo2b1drVkVjM2N3TmJFUVUzSmQteVdwSUJwRVpmaldFYllKWFladGgwQUI5ZG5naDU1cXhxdVdKMXlYTFhiSHVwOHdDRFcxN2lzSGdXLWo0UU9PZm84NzQ1NGpHWHNoY2JGUlFtM1N5THA0eGlYVE44VFNhTUU0NVM0c3FwbURvMFpHdnVlb2pKUTQyT3VmcFZ2MGN3aHRVLWhDYzlmZEF1ZEhiblBlWWY0OEdQbXVNbnpaN2MyODdhekRSSFZSbTRIb2g1eFVDdHliUFNNTGlHSUJ2Iiwib2F1dGhfdG9rZW4iOiJFQUFCd3pMaXhuallCQUZwWGxqcFdEeDBmeExLU2FYcXVqd2tuU2hNZGhYWGtNTDFWclpCaUFTTXozSElZczFzNjJ0YWg0aFpDbVJXeHRoWkJBdUF3Sng0ZG5IUnV3Rmo5VDh5Z0tva1pBNzg1bTE2cmZMeEN4cnpVSk9ZQU0yR2tsUjJLbEFoUjRQYzFtYjltUXBCdnRnczlRbnNUdWVjWkNVWkNzZmNuN2FHbGoyOHE1QXdOdGciLCJhbGdvcml0aG0iOiJITUFDLVNIQTI1NiIsImlzc3VlZF9hdCI6MTYyMDcyNjY3OX0; ds_user_id=2237911879; csrftoken=yPFKAwVoEdG9lugheIDRGKsCUQyQNrOx'}
			followers_list=get_followers_list(userid=userid,headers=viewer_cookie) #FETCH DATA

		# write_to_disk=mx.jdump(followers_list,f"./Data/{user}@{mx.datetime()}")
		mylist=[f'{x:20}' for x in followers_list]
		print('|'.join(mylist))

	if CALCULATE_MODE:
		calculate_difference('Data/_nikhil_swami_@test0','Data/_nikhil_swami_@test1')




	# url='https://i.instagram.com/api/v1/users/2280322955/info/'
	# p=mx.get_page(url,headers=headers).text
	# print(p)
	# attack_later=['suryagr_']#broadcast ashwant friend filth