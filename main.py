# Project purpose: Try Python to get and display electricity price
# Starting with tutorial: <https://www.scrapingbee.com/blog/web-scraping-101-with-python/>

import urllib.request
import socket
import re
import sys
import json

#### Functions

# Parse hostname
def get_host(host, local_port):
    plain_host = host.removeprefix("https://")
    plain_host = plain_host.rsplit('/')[0]
    print("HOST: " + plain_host)

    if(len(plain_host) == len(host)):
        plain_host = host.removeprefix("http://")
    if(len(plain_host) == len(host)):
    # localhost, set other port
        port = local_port
    else: 
        port = PORT
    return port,plain_host


# save to file
def save_response(response, filename = "../response.html"):
    # save response to file
    try:
        response_file = open(filename, "w")
        response_file.write(response)
        response_file.write("\n")
        response_file.close()
        print("response saved to " + filename)
    except:
        print("File write error")


# read from file
def read_file(filename):
    content = []
    try:
        file = open(filename, "r")
        content = file.read()
    except:
        print ("File open error")
        return None
    return content


#### Constants/variables
HOST = ""
LOCAL_PORT = 3000
PORT = 80

# Choose host by args: no args: localhost, np: nordpool.com, yl: yle.fi, -s: save response
HOST_ARGS = ["-lh", "-np", "-yl", "-il"]
HOST_LIST = list(HOST_ARGS)

hosts = read_file("hosts.json")
if(hosts != None):
    HOST_LIST = json.loads(hosts)
else:
    HOST_LIST[0] = "127.0.0.1"
print(HOST_LIST)

HOST_DICT = {
    HOST_ARGS[0]: HOST_LIST[0],
    HOST_ARGS[1]: HOST_LIST[1],
    HOST_ARGS[2]: HOST_LIST[2],
    HOST_ARGS[3]: HOST_LIST[3]
}


#### Script start
print("\n Valid arguments for choosing host are the following:")
print(HOST_DICT.keys())
print()

host_index = 0
good_arg = 0
saving_on = False

# choose host and saving
for a in sys.argv:
    if (a == "-s"):
        saving_on = True
    try:
        host_index = HOST_ARGS.index(a)
        good_arg = host_index
    except ValueError:
        host_index = good_arg # default to localhost
HOST = HOST_LIST[host_index]

# urllib experiment
# resolve port and host
PORT, plain_host = get_host(HOST, LOCAL_PORT)
# get response
response_obj = urllib.request.urlopen("http://" + plain_host + ":" + str(PORT), data=None, timeout=6.0)
# print((response_obj.headers))
try:
    c_type = response_obj.headers["Content-Type"]
except:
    c_type = ""

# to string
response_str = str(response_obj.read())

# save response to file with id (first number sequence as id)
response_id = re.search("\d+", response_str).group() 

if (response_id != None):
    print("Content contains: " + response_id)
    file_type = "" # from header
    if(c_type.endswith("html")):
        file_type = ".html"
    else:
        file_type = ".txt"

    if (saving_on):
        save_response(response_str, "./data/response" + str(response_id) + file_type)

# TODO find data
exit("done")

##############################
# socket experiment
# print("HOST: " + plain_host)

# setup header
accept_header = "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
# req_header = "GET / HTTP/1.1\r\nHost: 127.0.0.1\r\nAccept: text/html\r\n"
req_header = "GET / HTTP/1.1\r\nHost: {}\r\nAccept: {}\r\n".format(plain_host, accept_header)
# TODO fix formatting

# byte header
req_header_b = bytes(req_header, 'utf8')
print(req_header_b)
if("{" in req_header):
    exit("Invalid header - exiting")

#create socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
dest_address = (plain_host, PORT)
# print(socket.getaddrinfo(plain_host, PORT))

# connect
print("connecting")
client_socket.connect(dest_address)

# request
print("sending")
client_socket.sendall(req_header_b)

# receive response
# TODO broken again
response = ''
print("waiting for response")
failed_recv = False
while True:
    recv = client_socket.recv(1024)
    if not recv:
        failed_recv = True
        break
    response += str(recv)

# shutdown socket TODO

# close socket
client_socket.close()
save_response(response)
