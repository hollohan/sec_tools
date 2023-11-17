#!/usr/bin/python



# parse header
# only parsing request, host, content-type, cookies[FIXME]
def parse_header(h):
    r_headers = {}
    # POST URL HTTP/1.1
    line = h[0].split(' ')
    r_headers['method'] = line[0]
    r_headers['url'] = line[1]
    r_headers['protocol_version'] = line[2]


    these_headers = ['Host:', 'Content-Type:', 'Cookies:']
    for line in h[1:]:
        line = line.split(' ')
        if line[0] in these_headers:
            r_headers[line[0][:-1]] = [*line[1:]] # strip trailing : on line[0]

    # for thing in r_headers: print(f'{thing}: {r_headers[thing]}')
    return r_headers


# parse copied burp post
def parse_raw(raw):
    raw = raw.split('\n') # split lines

    loc = raw.index('')
    header = raw[:loc]   # header is beinning til first blank line
    body = raw[loc+1:]  # body is everything after first blank line
    #print(f'{header=}')
    #print(f'{body=}')
    headers = parse_header(header)



raw_post = '''POST /index.php/jobs/apply/8/ HTTP/1.1
Host: tenten.htb
Content-Length: 2140
Cache-Control: max-age=0
Upgrade-Insecure-Requests: 1
Origin: http://tenten.htb
Content-Type: multipart/form-data; boundary=----WebKitFormBoundaryClhcR0rFYfl5GoKQ
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.5672.93 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Referer: http://tenten.htb/index.php/jobs/apply/8/
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9
Connection: close

------WebKitFormBoundaryClhcR0rFYfl5GoKQ
Content-Disposition: form-data; name="jobman-apply"

1
------WebKitFormBoundaryClhcR0rFYfl5GoKQ
Content-Disposition: form-data; name="jobman-jobid"

8
------WebKitFormBoundaryClhcR0rFYfl5GoKQ
Content-Disposition: form-data; name="jobman-categoryid"


------WebKitFormBoundaryClhcR0rFYfl5GoKQ
Content-Disposition: form-data; name="jobman-field-2"

a
------WebKitFormBoundaryClhcR0rFYfl5GoKQ
Content-Disposition: form-data; name="jobman-field-3"

a
------WebKitFormBoundaryClhcR0rFYfl5GoKQ
Content-Disposition: form-data; name="jobman-field-4"

a@a.com
------WebKitFormBoundaryClhcR0rFYfl5GoKQ
Content-Disposition: form-data; name="jobman-field-6"


------WebKitFormBoundaryClhcR0rFYfl5GoKQ
Content-Disposition: form-data; name="jobman-field-7"


------WebKitFormBoundaryClhcR0rFYfl5GoKQ
Content-Disposition: form-data; name="jobman-field-8"


------WebKitFormBoundaryClhcR0rFYfl5GoKQ
Content-Disposition: form-data; name="jobman-field-9"


------WebKitFormBoundaryClhcR0rFYfl5GoKQ
Content-Disposition: form-data; name="jobman-field-10"


------WebKitFormBoundaryClhcR0rFYfl5GoKQ
Content-Disposition: form-data; name="jobman-field-11"


------WebKitFormBoundaryClhcR0rFYfl5GoKQ
Content-Disposition: form-data; name="jobman-field-14"


------WebKitFormBoundaryClhcR0rFYfl5GoKQ
Content-Disposition: form-data; name="jobman-field-15"


------WebKitFormBoundaryClhcR0rFYfl5GoKQ
Content-Disposition: form-data; name="jobman-field-16"; filename="aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa.txt"
Content-Type: text/plain

hi!:)

------WebKitFormBoundaryClhcR0rFYfl5GoKQ
Content-Disposition: form-data; name="jobman-field-18[]"

I have read and understood the privacy policy.
------WebKitFormBoundaryClhcR0rFYfl5GoKQ
Content-Disposition: form-data; name="submit"

Submit Your Application
------WebKitFormBoundaryClhcR0rFYfl5GoKQ--
'''

parsed_req = parse_raw(raw_post)