https://www.facebook.com/photo.php?fbid=10211372052247307&set=a.4939063284676.1073741830.1541466818&type=3


* install pip
* install facebook-sdk


* virtualenv?
* bbedit?
* git?

http://facebook-sdk.readthedocs.io/en/latest/install.html
http://facebook-sdk.readthedocs.io/en/latest/api.html
https://developers.facebook.com/docs/graph-api/overview
https://developers.facebook.com/docs/graph-api/explorer/
https://developers.facebook.com/docs/graph-api/reference
https://developers.facebook.com/docs/graph-api/using-graph-api/#paging



def SalvaFoto(photo_url, photo_name, album_name):
    dir = os.path.join(destinazione, album_name)
    if not os.path.exists(dir):
        os.makedirs(dir)
        
    req = requests.get(photo_url)
    with open(os.path.join(dir,photo_name) + ".jpg","w") as f:
        f.write(req.content)



# loop through list of all pictures and save; disabled for now because this is slow (~1sec/photo)(
# save_all_photos(photo_ids)


#print best_image_height
#print json.dumps(photo_data['images'], indent=4, sort_keys=True)
#print os.path.exists(dir)
# https://github.com/mattia-beta/Facebook-Albums-Downloader/blob/master/download_photos.py


# fields with ?
# edges with /



# https://graph.facebook.com/709246

# now i need to get an access token!


#print photo_id
#print graph.get_object(photo_id)
# https://www.facebook.com/photo.php?fbid=10100950287073888 -- i can see the photo here. how to download???



# First, need to figure out the Page ID of my facebook page.
# https://www.facebook.com/karina.pikhart
# right click profile picture > copy link address
# https://www.facebook.com/photo.php?fbid=10101453821856148&set=a.610124448558.2149115.709246&type=3&source=11&referrer_profile_id=709246
# https://www.facebook.com/709246 - that's my profile page ID!!!
# SUCCESS!!!

# But still need to get an access token to access (read/write) anything on this page...
# https://developers.facebook.com/docs/facebook-login/access-tokens
# https://graph.facebook.com/709246/photos
# {
#    "error": {
#       "message": "An access token is required to request this resource.",
#       "type": "OAuthException",
#       "code": 104,
#       "fbtrace_id": "BX1TSr8OD+c"
#    }
# }

# https://graph.facebook.com/me/accounts
# {
#    "error": {
#       "message": "An active access token must be used to query information about the current user.",
#       "type": "OAuthException",
#       "code": 2500,
#       "fbtrace_id": "ANLnkQWSPqC"
#    }
# }

# Before I can get an access token, it seems I need to figure out my 'app secret'
# https://developers.facebook.com/docs/facebook-login/security/
# Created a facebook developer (app) account
# https://developers.facebook.com/apps/1139781582844246/add/
# app secret = b2b131cf973211f6014e0f530c30f915
# DO NOT LEAVE THIS EXPOSED!!!

# doesn't work: https://graph.facebook.com/endpoint?key=value&access_token=709246|b2b131cf973211f6014e0f530c30f915
# https://graph.facebook.com/oauth/access_token?client_id=709246&client_secret=b2b131cf973211f6014e0f530c30f915&grant_type=client_credentials
# https://graph.facebook.com/oauth/access_token?client_id=1139781582844246&client_secret=b2b131cf973211f6014e0f530c30f915&grant_type=client_credentials
# TA DAAAAA: {"access_token":"1139781582844246|tpOauPvuNf81K6BDWP2_9qV8qus","token_type":"bearer"}


#graph = facebook.GraphAPI(access_token="1139781582844246|tpOauPvuNf81K6BDWP2_9qV8qus")
# https://stackoverflow.com/questions/24985441/facebook-graphapierror-an-active-access-token-must-be-used-to-query-information


# print type(graph)
# resp = graph.get_object('me/accounts')
#resp = graph.get_object('me?fields=id,name')
# resp = graph.get_object('709246?fields=id,name,gender,birthday') # https://developers.facebook.com/docs/graph-api/reference/user
# resp = graph.get_object('me?fields=id,name,gender,birthday')
# resp = graph.get_object('10100484595748038?fields=id,name,gender,birthday')
# resp = graph.get_object('709246/photos')
# 
# 709246 doens't seem to be working. 'me' and 10100484595748038 seem to be working (which I got from the result of some of these get calls)
# print type(resp)
# print resp
# print json.dumps(resp, indent=4, sort_keys=True)

# looks like the json result for photos are paginated - need to traverse through all the pages - https://developers.facebook.com/docs/graph-api/using-graph-api/#paging

#photo_url = "https://scontent.xx.fbcdn.net/v/t1.0-9/13892276_10100927778840568_1664575340537256113_n.jpg?_nc_cat=0&oh=d4c6e76ead5f9643d5c473ef6916addf&oe=5BBAC63F"


	# photo_url = 'https://www.facebook.com/photo.php?fbid=' + photo_id
	# print photo_url
	# from GET call: 10100927778840568?fields=images,link