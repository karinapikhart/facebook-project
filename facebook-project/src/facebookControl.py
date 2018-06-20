# LESSONS LEARNED FROM THIS PROJECT
# 1. This is definitely an example of a project where I could have done the tedious task WAY faster than the time it took me to automate the task with a script. If you're in it for the learning, NBD.
# 2. Your approach might hit some dead ends.
#    * Using facebook developer APIs (GraphAPI) - seems they've tightened their security and no longer let me access photos that my friends posted of me
#    * Using python requests package - I got stuck figuring out how to log into facebook
#    * Using selenium
# 3. Troubleshooting goes better when:
#    * You think systematically, simply, and clearly. You check obvious things. You find ways to compare something unknown to something known. You sanity check.
#      e.g. I was stuck in not understanding why my 'requests' call wasn't returning sensible results. Should have thoguht to save the result as an html file, and open the file. Would have seen that the page was locked behind a login screen, hence the 404 error. 
#    * You ask obvious/simple questions
#    * You don't get frustrated with yourself / stressed
#    * You google search the exact symptom you are seeing, rather than the underlying science/topics. Come back to learn the science later. Write code and then you'll learn how stuff works... not the other way around.
# 4. Save time by workspace optimizations:
#    * Opening up python through the command line saved me time for testing lines of code to see if they work. That was faster than rerunning the script every time, which was slow due to authentication steps and sleeps
#    * TextWrangler needed an update and thus required me to click a box every time I saved my file. Such a time sink!
#    * learning about virtual environments, PATH variables, etc., so that stuff doesn't slow me down
# 5. Front end vs back end stuff is a whole other world. Developers who are pros at one may not know the other.
# 6. How to make this project usable to the average computer user who doesn't have python??
# 7. Is this a misuse of selenium? Selenium appears to be a tool for writing software tests (e.g. to test your webpage?). If it didn't exist, what would I do?

import sys
import requests
from lxml import etree, html

import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

####################
## DEFINE GLOBALS ##
####################

WEBSITE = 'https://www.facebook.com'
USERNAME = 'karina.pikhart'
PHOTOS_PAGE = WEBSITE + '/' + USERNAME + '/photos'
EMAIL = 'karina.pikhart@gmail.com'

######################
## DEFINE FUNCTIONS ##
######################

def save_image(photo_id, url, destination_folder):
	req = requests.get(url) # to learn more about the http protocol's methods: https://www.w3schools.com/tags/ref_httpmethods.asp
	with open(destination_folder + '/' + photo_id + '.jpg', 'w') as f:
		f.write(req.content)

##########
## MAIN ##
##########

# ending notes for 6/19:
# * even with the sleeps, hit another Element is not clickable exception at image #126. Need to handle this exception
# * would be great to save some extra metadata such as: the name of the person who posted it, the date, and the caption or album name
# * would be great to have the authentication automated.
# * some of the images came out rather small. See if I can figure out if I'm getting the biggest image

browser = webdriver.Chrome()
browser.get(WEBSITE)

# print "Opened facebook..."
# a = browser.find_element_by_id('email')
# a.send_keys(EMAIL)
# print "Email Id entered..."
# b = browser.find_element_by_id('pass')
# b.send_keys(raw_input('enter your password for ' + WEBSITE + '...'))
# print "Password entered..."

raw_input('once you are logged in, press enter')
browser.get(PHOTOS_PAGE)
time.sleep(1)

# elem = browser.find_element_by_tag_name("body")
# 
# no_of_pagedowns = 20 # not enough! need a better way to know how many is enough!
# while no_of_pagedowns:
#     elem.send_keys(Keys.PAGE_DOWN)
#     time.sleep(1)
#     no_of_pagedowns-=1

images = browser.find_elements_by_css_selector('i.uiMediaThumbImg')
completed_images = []
pic_urls = []
more_images = True
counter = 0
while more_images:
	for image in images:
		counter += 1
		print 'clicking on image...'
		print image
		time.sleep(1)
		# without the sleeps, you eventually hit an exception in this loop. sleeps seemed to mitigate:
		# selenium.common.exceptions.WebDriverException: Message: unknown error: Element is not clickable at point (211, 1007)
		image.click() 
		time.sleep(1)
		main_body = browser.find_element_by_tag_name("body")
		spotlight_pics = browser.find_elements_by_css_selector('img.spotlight')
		if len(spotlight_pics) == 1:
			pic_url = spotlight_pics[0].get_attribute('src')
			pic_urls.append(pic_url)
		else:
			print 'hm...'
		completed_images.append(image)
		main_body.send_keys(Keys.ESCAPE)
	
	images = []
	all_images = browser.find_elements_by_css_selector('i.uiMediaThumbImg')
	more_images = False
	for image in all_images:
		if image not in completed_images:
			images.append(image)
			more_images = True
		

print counter

for url in pic_urls:
	save_image(url.split('/')[-1].split('.jpg')[0], url, '/tmp/pix')

# browser.close()
# browser.quit()

sys.exit()




################################################################################
################################################################################
################################################################################
################################################################################


# DEFINE GLOBALS
ACCOUNT_NAME = 'karina.pikhart'



# 1. Inspect source of my photos page:

# NEED TO FIGURE OUT HOW TO GET ALL DYNAMIC CONTENT LOADED (e.g. when you scroll)
url = 'https://www.facebook.com/' + ACCOUNT_NAME + '/photos' 
#s = requests.Session()
#req = s.get(url)

req = requests.get(url)

#print req # http status
#print req.content[:100]
#print len(req.content)

with open('/tmp/test.htm', 'w') as f:
	f.write(req.content)

sys.exit()



# for now, just load the content from a .htm file
with open('/Users/Karina/Dropbox/Projects/FacebookPhotoDownloader/facebook-project/src/Karina Pikhart.htm', 'r') as f:
	webpage_content = f.read()

#print type(webpage_content)
#print len(webpage_content)
#print type(html_page_content)
#print(etree.tostring(html_page_content, encoding='unicode', pretty_print=True))
#print webpage_content[:100]

# 2. Look for text containing...
#href="https://www.facebook.com/photo.php?fbid=10211372052247307"
#OR
#id="pic_10211372052247307"
#This will give you the IDs to all the pictures

# EXAMPLE
# image ID: 10212758856592553
# photo page: https://www.facebook.com/photo.php?fbid=10212758856592553&set=t.709246&type=3&theater
# URL where photo is: https://scontent-sea1-1.xx.fbcdn.net/v/t1.0-9/32533588_10212758856632554_5098108987597914112_n.jpg?_nc_cat=0&_nc_eui2=AeFzdAbrhjyyVEZZmGJyILZGnEq8Rm_MtpDIJqkLqyd9t1oCc6LV2NG0iXhV5bIy5U1uc1mT5o8JyqJ_ortHhOhV-sPS4QlsGqKoqdYo4OPtGQ&oh=e87c91f7e570669adcb37b11792209b3&oe=5BAB3A4D

#split_content = webpage_content.split('data-fbid="') # should learn a better way to parse/read/find stuff in html

split_content = webpage_content.split('<a')
photo_ids = []
for entry in split_content[1:]: # skip the first entry. this will break if you don't have >1 entry...
	split_a = entry.split('id="pic_')
	if len(split_a) > 1:
		id = split_a[1].split('"')[0]
		photo_ids.append(id)

# print len(photo_ids)
# print photo_ids[:10]
# sys.exit()

#photo_ids = []
#for entry in split_content[1:]: # skip the first entry
#	photo_ids.append(entry.split('"')[0])

photo_urls = []
for photo_id in photo_ids:
	photo_url = 'https://www.facebook.com/photo.php?fbid=' + photo_id + '&theater'
	photo_urls.append(photo_url)

#3. Go to that URL. Inspect source of that page, and look for text containing... 
#"
#src="https://scontent-dfw5-2.xx.fbcdn.net/v/t1.0-9/33766963_10211372052407311_260956311619895296_n.jpg?_nc_cat=0&amp;oh=077650a712d486ad3c6586c9548c2f46&amp;oe=5B7A43E8
#"


#//*[@id="photos_snowlift"]/div[2]/div/div[1]/div[1]/div[1]/div[1]/div[3]/img
#<img class="spotlight" alt="Image may contain: 5 people, including Lizzie Ridder, Katie McCormick and Karina Pikhart, people smiling, people standing and indoor" aria-busy="false" src="https://scontent-sea1-1.xx.fbcdn.net/v/t1.0-9/33766963_10211372052407311_260956311619895296_n.jpg?_nc_cat=0&amp;_nc_eui2=AeH78UywiJlxtWieM4qihqxrn8siv-DgsNzC6ah6aRpOc0WWGZl0fp07yLGs78mDwmIsGsVWX-7d3UYBo4Hlv0DqM0KAP8pzNv8vo3rjpgOmZQ&amp;oh=7544db09beb15d47fac2cd0cae7a5796&amp;oe=5BA1D0E8" style="width: 960px; height: 720px;">
#photos_snowlift > div._n9 > div > div.fbPhotoSnowliftContainer.snowliftPayloadRoot.uiContextualLayerParent > div.clearfix.fbPhotoSnowliftPopup > div.stageWrapper.lfloat._ohe > div.stage > div._2-sx > img


photo_url = 'https://www.facebook.com/photo.php?fbid=10211372052247307&theater'
req = requests.get(photo_url)
tree = html.fromstring(req.content)
#test = tree.xpath('img.spotlight')
#test = tree.xpath('//*[@id="photos_snowlift"]/div[2]/div/div[1]/div[1]/div[1]/div[1]/div[3]/img')
print type(tree)
print len(tree)
print tree
#print type(req)
#print type(test)
#print test

sys.exit()

photo_locations = []
for photo_url in photo_urls[:10]: # for testing
#for photo_url in photo_urls:
	print 'now looking at ' + photo_url

	# https://docs.python.org/3/tutorial/errors.html
	try: 
		req = requests.get(photo_url)
	except:
		print '  exception enountered! skipping this url'
		# https://docs.python.org/2/tutorial/controlflow.html#break-and-continue-statements-and-else-clauses-on-loops
		continue
	
	photo_file = req.content.split('<img class="spotlight"')[1]  # should learn a better way to parse/read/find stuff in html
	#for photo_file in photo_files[1:]: # skip the first one
		# print photo_file[:1000]
		#print '  now looking for images on this page...'
	photo_location = photo_file.split('src="')[1].split('"')[0]
	
		#if 'scontent' in photo_location:
	print photo_location
	photo_locations.append(photo_location)
	
	
# img.spotlight	

print len(photo_locations)
print photo_locations

# 4. Go to that URL. Download the image

for photo_location in photo_locations:
	#NOPE! Get "Bad URL date param" #Hm... if I strip out the two instances of "amp;" in the URL from step 3 that didn't work... then it works!!! Why??!!
	photo_location = photo_location.replace('&amp;', '&') # string.replace(s, old, new[, maxreplace]) https://docs.python.org/2/library/string.html	
	save_image(photo_location.split('.jpg')[0].split('/')[-1], photo_location, '/tmp')


##########################################################################################

#for photo_id in photo_ids:
#	print photo_id

#help(requests.models.Response)
#print url
#print req
#print req.status_code
#print type(req)
#print type(req.content)
#print type(req.text)
#print len(req.content)
#print req.__attrs__

# i = 1
# for l in req.iter_lines():
# 	print i, l[:300]
# 	i += 1

#print req.content
#print req.content[:100]
#print req.content[len(req.content)-100:]
#print req.content.count('https://www.facebook.com/photo.php?fbid=')
#print req.content.count('pic_')
#print req.content.count('fbid=')
#print req.content.count('fbid')
#print req.text.count('data-fbid')
#print req.content.count('link')
#print req.content.count('uiMediaThumbImg')
#print req.content.count('404')
#print '*****'
#print req.content