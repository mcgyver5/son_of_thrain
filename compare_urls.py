"""
1. open file
2. pull all urls into map or list via regex
3. use git API to look at remote file  from github / gitlab
4. make list of urls from that file
5. result is format like 'Your file is missing the following URLs that the remote repo has and your file has the following urls that the 
remote repo is missing.'

"""
import os.path
from os import path
import sys
import getopt
import re
import requests
from collections import Counter

def print_results(desc,results):
    section_separator = "\r\n-----------------------------------------------------------------------------------\r\n"
    result_string = "The {} list has the following {} URLs that the {} list does not have:"
    if desc == "right":
        result_string = result_string.format("remote",len(results),"local")
    if desc == "left":
        result_string = result_string.format("local",len(results),"remote")
    if desc == "middle":
        result_string = "The lists have the following {} URLs in common: ".format(len(results))
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
local_file = ""
if len(sys.argv) > 2:
    local_file = sys.argv[1]
    if path.exists(local_file):
        print(local_file + " exists ")
    else:
        print(local_file + " does not exist")
        sys.exit()
else:
    print("usage: python compare_urls.py local_file remote_file")
    sys.exit()
url_list = []
fh = open(local_file)
for line in fh:
    url = find_url(line)
    if url:
        url_list.append(url[0])

remote_list = []
remote_url = sys.argv[2]
#remote_url = "https://raw.githubusercontent.com/sanjacinto/excellent_training_videos/master/README.md"
r = requests.get(remote_url, allow_redirects=True)
for s in r:
    url = find_url(s)
    if url:
        remote_list.append(url[0])

left_result = list((Counter(url_list) - Counter(remote_list)).elements())
right_result = list((Counter(remote_list) - Counter(url_list)).elements())
remote_set = set(remote_list)
local_set = set(url_list)

middle_result = local_set & remote_set 

print_results("right",right_result)
print_results("left",left_result)
print_results("middle",middle_result)

