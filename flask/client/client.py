import requests
import os
import sys
# TODO
# copy directory structure
# relative links to not break dataseets?
# look into proper string and packet sanitization
# index gui + results graphs 

base_url = 'http://localhost:5000/'
upload_url = 'upload'

def send_file(path):
    upload_file = open(path,'rb')
    data = {'file' : upload_file}
    return requests.post(url = base_url + upload_url, files = data)

def send_mkdir(path):

def send_directory(path):
    for root, directories, filenames in os.walk(path):
        for filename in filenames: 
            upload_file = os.path.join(root,filename)
            print(upload_file)
            print(send_file(upload_file))

send_directory(sys.argv[1])

