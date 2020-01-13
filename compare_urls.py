"""
1. open file
2. pull all urls into map or list via regex
3. use git API to look at remote file  from github / gitlab
4. make list of urls from that file
5. result is format like 'Your file is missing the following URLs that the remote repo has and your file has the following urls that the 
remote repo is missing.'

"""
import re
import requests
from collections import Counter

def find_url(string):
    url = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', string) 
    return url

fh = open("my_test_links.txt")
url_list = []
for line in fh:
    url = find_url(line)
    if url:
        url_list.append(url[0])
for u in url_list:
    print(u)

remote_list = []
remote_url = "https://raw.githubusercontent.com/sanjacinto/excellent_training_videos/master/README.md"
#remote_url = "https://github.com/sanjacinto/excellent_training_videos/blob/master/README.md"
r = requests.get(remote_url, allow_redirects=True)
for s in r:
    url = find_url(s)
    if url:
        remote_list.append(url[0])

for link in remote_list:
    print(link)

left_result = list((Counter(url_list) - Counter(remote_list)).elements())
right_result = list((Counter(remote_list) - Counter(url_list)).elements())
remote_set = set(remote_list)
local_set = set(url_list)

middle_result = local_set & remote_set 


print("the remote list has the following URLs that the local one does not have:")
print(str(right_result))
print("your list has the following URLS that the remote list does not have")
print(str(left_result))
print("both lists contain the following URLs:")
print(str(middle_result))
