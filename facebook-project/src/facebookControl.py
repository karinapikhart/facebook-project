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