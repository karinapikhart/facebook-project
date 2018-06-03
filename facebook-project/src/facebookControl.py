# Created by Karina Pikhart on 2018/06/03

import facebook
import json
import os
import requests # http://docs.python-requests.org/en/master/
import logging

# gets all the objects at the edges of a base object
# handles pagination in the results
# path is the path to the objects of interest, typically '<node>/<object>?fields=<field1,field2,field3>'
def fetch(path):
	data = []
	more_pages = True
	current_page = path
	
	while more_pages:
		resp = graph.get_object(current_page)
		data += resp['data']
		
		if 'next' in resp['paging']:
			current_page = path + '&after=' + resp['paging']['cursors']['after']
		else:
			more_pages = False			
			
	return data

# loops through the photo's image field ('image field' is a list of images)
# returns the URL of the image with the largest height
# TO DO:
#   exception handling: what to do if we still have an empty string at the end?
def get_largest_image_url(image_list):
	best_image_height = 0
	image_url = ''
	for image in image_list:
		if image['height'] > best_image_height:
			best_image_height = image['height']
			image_url = image['source']
	return image_url 

# saves the .jpg from the URL provided, to the folder provided, using the facebook Object ID as the filename
# TO DO:
#   speed this up? per logging, this is a pretty slow operation. (1/2 sec per image)
#   do better file/directory handling. maybe with a GUI. this doesn't check for the existence of the directory. directory is hard coded. likely overwrites images if they are already there
#   see if I can save some additional metadata, e.g. the accurate create_date
#   exclude anything that I uploaded (just save other people's pictures)
#   download entire albums where I am tagged in an image in that album (e.g. Yi's wedding)
def save_image(photo_id, url, destination_folder):
	req = requests.get(url) # to learn more about the http protocol's methods: https://www.w3schools.com/tags/ref_httpmethods.asp
	with open(destination_folder + '/' + photo_id + '.jpg', 'w') as f:
		f.write(req.content)

# takes a list of photo metadata from facebook, and saves the a copy of each photo locally
# TO DO:
#   this assumes that 'id' and 'images' fields are present
def save_all_photos(photo_data):
	i = 1
	total = len(photo_data)
	for photo in photo_data:
		photo_url = get_largest_image_url(photo['images'])
		save_image(photo['id'], photo_url, DIRECTORY + '/downloadedPhotos/testFolder')
		logging.info('Saved image %d of %d' % (i, total))
		i += 1
        
if __name__ == "__main__":	
	LOGGING_LEVEL = logging.DEBUG
	DIRECTORY = '/Users/Karina/Dropbox/Projects/FacebookPhotoDownloader'
	NODE = 'me'
	
	logging.basicConfig(filename=DIRECTORY + '/facebook-project/logs.log',level=LOGGING_LEVEL, format='%(asctime)s %(levelname)s: %(message)s')
	logging.info('hello world!')
	
	ACCESS_TOKEN = raw_input("What is the access token to your facebook page? You can get a user access token here: https://developers.facebook.com/tools/explorer/. ")
	logging.info('received ACCCESS_TOKEN from user')
	
	graph = facebook.GraphAPI(access_token=ACCESS_TOKEN)
	ACCOUNT_ID = graph.get_object(NODE)['id']
	NODE = ACCOUNT_ID

	edge = 'photos'
	fields = 'id,created_time,from,height,width,images,link,webp_images'
	
	logging.info('fetching all photos from user')
	photo_data = fetch(NODE + '/' + edge + '?fields=' + fields)
	logging.info('fetching complete. found %d photos' % len(photo_data))
	
	# TROUBLESHOOTING:
	# hm, i don't seem to be getting photos that my friends have tagged me in. why??
	# i only get photos i uploaded, and that businesses uploaded (e.g. photos that are 'public', not 'private')
	# https://developers.facebook.com/docs/graph-api/reference/user/photos/
	photo_uploader = {}
	for photo in photo_data:
		uploader_name = photo['from']['name']
		if uploader_name in photo_uploader.keys():
			photo_uploader[uploader_name] += 1
		else:
			photo_uploader[uploader_name] = 1
	print photo_uploader

	# DISABLING WHILE I TROUBLESHOOT ABOVE
	#logging.info('saving all photos...')
	#save_all_photos(photo_data)
	
	logging.info('goodbye world!')

