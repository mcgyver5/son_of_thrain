from bs4 import BeautifulSoup
import os
from os import path
import sys
import re
import requests
from collections import Counter

class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

### HINT, to use a remote github file as a comparision to a local:
### right click on remote file and copy URL
### also can compare two github files with one another.

def print_results(desc,results):
    # instead of right left middle use remote, local, shared
    section_separator = "\r\n-----------------------------------------------------------------------------------\r\n"
    other = "remote"
    
    if desc == "remote":
        other = "local"
    
    if desc == "middle":
        result_string = "The lists have the following {} URLs in common: ".format(len(results))
    else:
        result_string = color.BOLD + "The {} list has the following {} URLs that the {} list does not have:" + color.END
        result_string = result_string.format(desc,len(results),other)
    none_result = "The {} list is empty".format(desc)
    if len(results) > 0:
        print(result_string)
        for url in results:
            print(url)
    else:
        print(none_result)
    print(section_separator)

def find_url(string):
    url = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', string) 
    return url
def get_pastebin_list(pastebin_url):
    remote_text = requests.get(pastebin_url,'').text
    soup = BeautifulSoup(remote_text,'lxml')
    results = soup.find("textarea")
    result_list = str(results.text).splitlines()

    filtered_list = [line for line in result_list if line.startswith('http')]

    return filtered_list

def get_github_list(github_url):
    pass

def build_remote_list(remote_url):
    # pastebin url is like:  https://pastebin.com/MfdUqsyE
    if remote_url.startswith('https://pastebin'):
        result_list = get_pastebin_list(remote_url)
        return result_list
    remote_list = []
    response = requests.get(remote_url, allow_redirects=True)

    try:
        print(response.raise_for_status())
        response_text = response.text
    except requests.exceptions.HTTPError as err:
        print(err)
        sys.exit(1)
    #following is for github:
    soup = BeautifulSoup(response_text,'lxml')
    results = soup.find("article")
    anchors = results.find_all("a")
# opp for list comprehnsion:
    remote_list = [anchor['href'] for anchor in anchors if anchor['href'].startswith('http')]
    '''
    for anchor in anchors:
        url =  anchor['href']
        if url.startswith("http"):
            remote_list.append(url)
    '''
    return list(set(remote_list))

def build_local_list(file_handle):

    local_list = []
    for line in fh:
        url = find_url(line)
        if url:
            local_list.append(url[0])
    return list(set(local_list))

local_file = ""
if len(sys.argv) > 2:
    local_file = sys.argv[1]
    if path.exists(local_file):
        print("\r\n")
    else:
        print(local_file + " does not exist")
        sys.exit()
else:
    print("usage: python compare_urls.py local_file remote_file")
    sys.exit()


fh = open(local_file)
local_list = build_local_list(fh)
remote_url = sys.argv[2]
remote_list = build_remote_list(remote_url)

print(color.UNDERLINE + "Comparing local file {} with remote file {} ".format(local_file,remote_url))
print(color.END)
left_result = list((Counter(local_list) - Counter(remote_list)).elements())
right_result = list((Counter(remote_list) - Counter(local_list)).elements())
remote_set = set(remote_list)
local_set = set(local_list)
middle_result = local_set & remote_set

print_results("remote",right_result)
print_results("local",left_result)
print_results("middle",middle_result)
