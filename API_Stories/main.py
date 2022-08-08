import os
import sys
sys.path.append('../')
from mxproxy import mx
import requests

def get_viewers_of_story(url,saveto=''):
	allusers=[]
	for maxid in [0,20,70,120]:
		resp=requests.post(url,data={'include_blacklist_sample':'false','max_id':maxid}, headers=mx.parse_raw_headers('headers.txt'))
		allusers.extend(resp.json()['users'])

	mx.jdump(allusers,path=saveto)
	return allusers

def get_difference_of_viewers(suspect,reference,reverse=0):
	filtering=lambda x:x['username']
	A=set(map(filtering, mx.jload(suspect)))
	B=set(map(filtering, mx.jload(reference)))
	# print(len(B))
	if not reverse:
		print(sorted(list(A-B)))
	else:
		print(sorted(list(B-A)))
	# print(-set(jload(reference)))

if __name__ == '__main__':

	INPUTS={
		'url' : 'https://i.instagram.com/api/v1/media/2899076877201808156/list_reel_media_viewer/',
		'outfile':'story_swamix_sunglasses_20220807.json',
		'outfile2':'sample_story_alizee.json'
	}

	# get_viewers_of_story(INPUTS['url'],saveto=INPUTS['outfile'])
	get_difference_of_viewers(INPUTS['outfile'],INPUTS['outfile2'],reverse=0)

