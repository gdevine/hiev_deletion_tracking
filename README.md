# Hiev Deletion Tracking

Python Script for tracking records deleted from HIEv
------------

The HIEv (DIVER) data capture application(https://github.com/IntersectAustralia/dc21), installed at HIE, University of Western Sydney, does not currently track
deletion of records. This python script uses the HIEv API to indirectly track such deletions by:

1. Doing a nightly JSON dump of all existing records 
1. Comparing this JSON dump with a JSON created from the day before
1. Appending details of any deleted records to file
     
### Notes ###
* The current script searches across a subset of all users (control PCs at HIE are omitted). You can remove this to search across all users.
* You must supply a HIEv API key
* The script currently only compares todays listings against a file dated from the day before. If a file does not exist for the day before, a comparison will not occur (i.e. 
the script will not continue to look backwards in time for the last existing file).  
