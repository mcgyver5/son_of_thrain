import re
f = open("shodan.txt")
ip_list = []
regex_ip_pattern = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')
for linex in f:
    try:
        ip_list.append(regex_ip_pattern.search(linex)[0])
    except:
        print("nonetype")
for entry in ip_list:
    print(entry)

