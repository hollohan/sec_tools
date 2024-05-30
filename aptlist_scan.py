
'''
    not sure how well this will work,
    but I want something to scan the output of an 'apt list'
    and tell me if any of those package versions are out of date
'''
import subprocess
from colorama import Fore, Style
import time

# line like -> zsh-syntax-highlighting/kali-rolling,now 0.7.1-2 all [installed,automatic]
# output like -> [ 'zsh-syntax-highlighting',  '0.7.1-2' ]
def parse_line(line):
    line = line.split()
    package = line[0].split('/')[0]
    version = line[1]
    return [ package, version ]


# with package name
# do 'apt-cache policy <package name>'
# parse output
# return version number
def get_apt_version(package):
    cmd = f'apt-cache policy {package}' # WARNING!!! -> this is vulnerable by default, make sure you trust the input !!!
    #print(f'{cmd=}')
    ps = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    stdout, stderr = ps.communicate()
    #print(f'{stdout=}')
    #print(f'{stderr=}')
    assert stderr == b'', f'error -> {stderr.decode("utf-8")}'
    assert stdout != b'', f'error -> :/'
    version = [x.strip() for x in stdout.split(b'\n') if b'Candidate: ' in x][0]
    version = version.split()[1]
    return version.decode('utf-8')

def read_file():
    # load file
    # parse files into list of package names and versions
    filepath = '/tmp/a/aptlist'
    packages = {} # [ { name, version } ]
    summary = { 'needs_update': 0, 'updated': 0 }
    with open(filepath, 'r') as file:
        for line in file.readlines():
            line = line.strip()
            #print(f'{line=}')
            # parse line
            package, version = parse_line(line)
            #print(f'{package=}')
            #print(f'{version=}')

            apt_version = get_apt_version(package)
            #print(f'{apt_version=}')

            if version != apt_version:
                print(f'{Fore.RED}update required [{package}] file=[{version}] apt=[{apt_version}]{Style.RESET_ALL}')
                summary['needs_update'] += 1
            else:
                print(f'{Fore.GREEN}updated [{package}] file=[{version}] apt=[{apt_version}]{Style.RESET_ALL}')
                summary['updated'] += 1

        #time.sleep(1)
        return summary


# with package name
# query apt-cache policy <pckgName>
# find the line starting with Version:
# get everything after the version
if __name__ == '__main__':
    summary = read_file()
    print(f'{summary["needs_update"]} packages need update, {summary["updated"]} all up to date')