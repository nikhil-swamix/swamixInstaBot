# Documentation of my messy code

### ask any doubts in issues, or directly open pull request so i will add your code here. 

## ABOUT (apiurlprefix):
		please note that variable (apiurlprefix) is url of my account,
		it may slightly differ for you,	to identify correct url, go to chrome, open inspect
		element, then go to	network tab, and open your instagram account and open followers
		tab, now the app (aka your browser) makes a request to server with your client api
		parameters. so as soon as you open your followers list, then check the latest request
		in network tab, that is the url you are looking for my friend, now check its response,
		it will be a JSON derulo. all stuff i have done here is parsing the json and calculating
		logical difference of followers aka tracking based on timestamps.
## About (userid):
		do not worry about userid, it can be fetched/resolved with
		'get_userid' function which i wrote above,	in the if main block below,
		just change the variable for example userid='_nikhil_swami_', rest assured handled. 
## ABOUT (headers):
		headers are sent with request module as request.get(url,headers={'apple':'ball'}), its basically,
		the method of sending mini data with each request, here our mini data is cookie , it helps the server to  
		identify you are you, like a id-card. so please get your cookie from the browser via  
		Browser->inspect_element->network_tab->Request_Headers->Cookie.