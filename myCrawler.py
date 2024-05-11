import sys
import requests
import argparse

# return a list of links found in content
def find_links(content, flag_start='href="', flag_stop='"'):
    keep_looking = True
    results = []
    while keep_looking:
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
def get_url(url):
    print(f'Loading {url}... ', end='')
    r = requests.get(url)
    if (r.status_code != 200):
        print(':(')
        return 0
    print(':)')
    return r.text

if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        prog='myCrawler',
        description='crawls websites for urls',
    )
    parser.add_argument('-u', '--url', help='the url to crawl', required=True)
    args = parser.parse_args()
    
    url = args.url

    flag_starts = [ 'href="', 'src="']
    urls_found = []

    pageBody = get_url(url)
    for flag_start in flag_starts:
        links = find_links(
            pageBody,
            flag_start=flag_start,
            flag_stop='"'
        )
        urls_found = [*urls_found, *links]

    urls_found = set(urls_found)

    print()
    print('--- urls found ---\n')
    for link in urls_found: print(link)