

import requests
from sys import argv


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



# usage: myPost.py <url> <wordlist>
if len(argv) != 3:
    print(f'usage: myPost.py <url> <wordlist>')
    exit()

wordlist = argv[2]
url = argv[1]
data = { 'user_login': 'FUZZ' }
f = lambda x: 'Invalid username or email' not in x 

post_n_find(url, data, f)