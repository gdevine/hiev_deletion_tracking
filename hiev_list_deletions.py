'''
Python script to perform a nightly HIEv search api call (to look at data inventory within HIEv) 
and compare the resulting json with json from the previous night in order to highlight data files 
deleted that day.

Author: Gerard Devine
Date: July 2015
'''

import os
import json
import urllib2
from datetime import date, datetime, timedelta
import time


# -- Set up global values
request_url = 'https://hiev.uws.edu.au/data_files/api_search'
api_token = 'YOUR-API-TOKEN'
date_today = datetime.now().strftime('%Y-%m-%d')
date_yesterday = (date.today() - timedelta(days=1)).strftime('%Y-%m-%d')
today_file = 'hiev_inventory_' + date_today + '.json'
yesterday_file = 'hiev_inventory_' + date_yesterday + '.json'
deletions_file = 'hiev_deleted-files.txt'

ctrl_pc_ids = [4, 7, 9, 85]  # IDs of the various facility PC uploaders that are omitted from the search 


# -- Create an empty list for gathering results
all_entries = []

# -- Loop through all users/uploaders apart from ctrl field PCs
for user_id in range(1,150):         #150 chosen as a high based on current number of users
  if user_id not in ctrl_pc_ids:  
    # -- Set up the http request
    request_headers = {'Content-Type' : 'application/json; charset=UTF-8', 'X-Accept': 'application/json'}
    request_data = json.dumps({'auth_token': api_token, 'uploader_id':str(user_id)})

    # -- Handle the returned response from the HIEv server
    request  = urllib2.Request(request_url, request_data, request_headers)
    response = urllib2.urlopen(request)
    js = json.load(response)
  
    # -- Loop through each dictionary entry in js and append it to the master list
    for entry in js:
      all_entries.append(entry)

# -- Create a new datestamped file (to be used in the following night's comparison), write the full json to it, and close it
with open(today_file, 'w') as today_data:
  json.dump(all_entries, today_data)
today_data.close()

# -- If a file exists for yesterday, ingest it and do a comparison, documenting any deleted files
if os.path.isfile(yesterday_file):   
  with open(yesterday_file) as yesterday_data:    
    yesterday_js = json.load(yesterday_data)
  
    deleted=''
    for x in yesterday_js:
      found = 'false'
      for y in all_entries:    # using the existing all_entries json
        if y['file_id'] == x['file_id']:
          found = 'true'
  	  break
      if found == 'false':
	      deleted += 'Date: ' + date_today + ', Record missing : ' + str(x['file_id']) + ', Filename: ' + str(x['filename']) + ', Data Start: '+ str(x['start_time']) + ', Data End: '+ str(x['end_time']) + ', Owner ID: ' + str(x['created_by_id']) + '\n'

    # write details of the deleted records to file
    with open(deletions_file, 'a') as deletion_data:
      deletion_data.write(deleted)
    deletion_data.close()

  # Close and delete yesterday's file as it is no longer needed
  yesterday_data.close()
  os.remove(yesterday_file)
  
# -- Else record that no file for yesterday was found
else:
  with open(deletions_file, 'a') as deletion_data:
    deletion_data.write('No file found for yesterday (' + date_yesterday + ') comparison\n')
  deletion_data.close()
