import socket
import argparse
import threading
import time

MAX = 16
semaphore = threading.Semaphore(MAX)

def check_host(host, port):
    semaphore.acquire()
    #print(f'trying {host}:{port}')
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
    try:
        s.connect((host, port))
        print(f':) {host}:{port}')
    except:
        pass
        #print(f'nope -> {host}:{port}')
    finally:
        semaphore.release()
        return

def scan_host(host):
    print('starting scan ...')
    for port in range(1, 0xffff):
        t = threading.Thread(target=check_host, args=(host, port))
        t.start()
        time.sleep(1/MAX)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='portscan in Python')
    parser.add_argument('-i','--ip', help='IP address of host to portscan', required=True)
    args = parser.parse_args()
    host = args.ip

    scan_host(host)