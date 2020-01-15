
import os
from os import path
import sys
import getopt
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


def print_results(desc,results):
    # instead of right left middle use remote, local, shared
    other = remote
    if desc == "remote":
        other = "local"
    section_separator = "\r\n-----------------------------------------------------------------------------------\r\n"
    result_string = color.BOLD + "The {} list has the following {} URLs that the {} list does not have:" + color.END
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
        print("\r\n")
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
r = requests.get(remote_url, allow_redirects=True)
print(color.UNDERLINE + "Comparing local file {} with remote file {} ".format(local_file,remote_url))
print(color.END)
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

