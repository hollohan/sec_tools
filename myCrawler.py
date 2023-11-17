import sys
import requests


# return a list of links found in content
def find_links(content):
    keep_looking = True
    results = []
    while keep_looking:
        flag_start = '<a href="'
        flag_stop = '"'
        loc_start = content.find(flag_start)
        if loc_start < 0: break
        loc_start += len(flag_start)
        loc_stop = content[loc_start:].find(flag_stop)

        match = content[loc_start:loc_start+loc_stop]
        results.append(match)

        content = content[loc_stop:]
    
    results = list(set(results))
    return results


# send a get request and return the data
def do_once(url):
    r = requests.get(url)

    print(f'{r.status_code=}')

    return r.text

url = 'https://myquickresource.com/'

a = do_once(url)
links = find_links(a)
for link in links: print(link)