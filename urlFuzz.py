import requests
import threading

''' engine '''
# send request to url and match response against conditions
def do_once(semaphore, url, conditions):
    with semaphore:
        r = requests.get(url)
        # filter out status codes
        is_match = [x(r) for x in conditions]
        if all(is_match):
            print(f'[{r.status_code}]: {url}')

# iterate a wordlist and call do_once with word-formatted url
def do_wordlist(base_url, filename, conditions):
    with open(filename, 'rb') as file:

        max_threads = 4
        semaphore = threading.Semaphore(max_threads)

        threads = []

        for word in file.readlines():
            word = word.strip().decode('utf-8')

            # threading.Thread(group=None, target=None, name=None, args=(), kwargs={}, *, daemon=None)
            t = threading.Thread(
                target=do_once,
                args=(semaphore, f'{base_url}{word}', conditions)
                )
            t.start()
            threads.append(t)
            #do_once(f'{base_url}{word}', conditions)

        for t in threads:
            t.join()


''' match/filter conditions '''
# returns true if status_code is in match_codes
def isMatch_statusCodes(r):
    match_codes = [
        200
    ]
    status_code = r.status_code
    if status_code in match_codes: return True
    return False

# returns true if status code is not in notmatch_codes
def notMatch_statusCodes(r):
    notmatch_codes = [
        404,
        403
    ]
    status_code = r.status_code
    if status_code not in notmatch_codes: return True
    return False


if __name__ == '__main__':
    url = 'http://usage.htb/'
    filename = '/home/user/wordlists/SecLists/Discovery/Web-Content/raft-large-words.txt'
    
    # a list of conditions that the response will be testedd against
    # each condition is a function that returns true or false
    # if all conditions return true, then the url will be displayed as a match
    conditions = [
        notMatch_statusCodes
    ]
    do_wordlist(url, filename, conditions)