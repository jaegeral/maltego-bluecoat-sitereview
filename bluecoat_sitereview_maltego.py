'''

Created: July 15, 2014
Created: July 15, 2014

Author: alexanderjaeger

This script contains the most comprehensive list of BlueCoatSitereview transforms.
Basic descriptions of each transform are at the bottom of this file.
Please check the documentation on GitHub for usage, inputs, and outputs.

To install: Copy the file in a folder (/home/user/maltego/bluecoat/

Maltego: 
Local Transformation --> 
	Name --> BlueCoat_SiteCheck_Maltego
	Description --> blank
	transformID --> alexanderjaeger.bluecoatmaltego
	Author --> alexanderjaeger
	Input entity type --> URL

'''

import os, sys
import requests
import json 
import urllib
import urllib2
import requests
from MaltegoClass import MaltegoTransform, EntityTypes
from BeautifulSoup import BeautifulSoup

#declare required params
bluecoat_base = "http://sitereview.bluecoat.com/rest/categorization"

##############################################################################################

def siteCheckCat(me, string_in):
    try:
	
	payload = {'url': string_in}
	
	me = MaltegoTransform()
	me.addUIMessage("starting fetch BlueCoat results!")     
	data = urllib.urlencode(payload)
	req = urllib2.Request(bluecoat_base + '', data)
	response = urllib2.urlopen(req)
	the_page = response.read()


	response_data = json.loads(the_page)
	me.addUIMessage("preparing Maltego object!")  
	
	thisent = me.addEntity("maltego.URL",string_in);
	
	for key, value in response_data.iteritems():
		if key == 'categorization':
			#parsing of categorization
			soup = BeautifulSoup(str(value))
			category=soup.a # will only use values between <a> tags
			thisent.addAdditionalFields(key,key,True,category.string)
			thisent.setValue("Bluecoat " + string_in + " " + category.string)
		elif key == 'ratedate':
			#parsing of ratedate
			stringsplit = str(value).split("<img") #Remove useless stuff
			thisent.addAdditionalFields(key,key,True,stringsplit[0])
		else:
			thisent.addAdditionalFields(key,key,True,str(value))
		
         
    except:
        me.addEntity(EntityTypes.textMessage, 'siteCheckCat Unknown Error:%sType: %s%sValue:%s' % 
                     (os.linesep, sys.exc_info()[0], os.linesep, sys.exc_info()[1]))
    return me




    
functions = {
             'siteCheckCat': siteCheckCat,       #check a page at Bluecoat

             }

##############################################################################################
###                                     MAIN                                               ###
##############################################################################################

if __name__ == '__main__':
    transform = sys.argv[1]
    data = sys.argv[2]    
    
    me = MaltegoTransform()
    
    m_result = functions[transform](me, data)
    m_result.returnOutput()

