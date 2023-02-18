# Project purpose: Get and display electricity price or other interesting data.
#
# Starting with tutorial: <https://www.scrapingbee.com/blog/web-scraping-101-with-python/>

import urllib.request
import socket
import re
import sys
import json
import sched, time
from filehandler import FileHandler
from responsehandler import ResponseHandler
from traffichandler import TrafficHandler as TH
from datahandler import DataHandler as DH


main_scheduler = sched.scheduler(time.time, time.sleep)

FH = FileHandler
CORE_PROPS_WINDOWS = "%PROGRAMDATA%/SteelSeries/SteelSeries Engine 3/coreProps.json"
CORE_PROPS_OSX = "/Library/Application Support/SteelSeries Engine 3/coreProps.json"
DRIVER_PATH = 'r"C:/webdriver"'

# GameSense message for illumination
color_message = {}

# GameSense address as "host:port"
gamesense_address = ""

#### Functions
def get_coreprops_filepath():
    if(sys.platform.startswith('win32')):
        return resolve_path_win(CORE_PROPS_WINDOWS)
    elif(sys.platform.startswith('darwin')):
        return CORE_PROPS_OSX
    else:
        print("Unsupported OS")
        return ""


def resolve_path_win(old_path):
    new_path = "C:/" + re.sub('%', '', old_path, count=2)
    return new_path


# get destination address
def get_destination_address(FH, get_coreprops_filepath):
    core_file = get_coreprops_filepath()

# read address from file
    core_content = FH.read_file(FH, core_file)
    if(core_content != None):
        core_json = json.loads(core_content) # to object
        return(core_json["address"])
    else:
        print("Props not found")
        return ""


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


#### Constants/variables
HOST = ""
LOCAL_PORT = 3001
PORT = 80

# Choose host by args: no args: localhost, np: nordpool.com, yl: yle.fi, -s: save response, ...
# mi: prod. prediction (fmi.fi)
HOST_ARGS = ["-lh", "-np", "-yl", "-il", "-fg", "-mi"]
HOST_LIST = list(HOST_ARGS)

hosts = FH.read_file(FH, "hosts.json")
if(hosts != None):
    HOST_LIST = json.loads(hosts)
else:
    HOST_LIST[0] = "127.0.0.1"

HOST_DICT = {}
a_max = min(len(HOST_ARGS), len(HOST_LIST))

# Create key-value dictionary of possible hosts
for a in range(a_max):
    HOST_DICT[HOST_ARGS[a]] = HOST_LIST[a]

# print(HOST_DICT)

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
        host_index = good_arg # revert to a good one
HOST = HOST_LIST[host_index]


# Load SteelSeries color format from file
color_json = FH.read_file(FH, "colordata.json")
if(color_json != None):
    try:
        color_message = json.loads(color_json)
    except ValueError:
        print("Error with JSON")
else: print("No data ")

# SteelSeries local address
gamesense_address = get_destination_address(FH, get_coreprops_filepath)

print("GameSense server: " + gamesense_address)
print("Color data:")
print(color_message)

# change color data for LED mouse
DH.change_data(color_message, "device-type", "mouse")
# DH.change_data(color_message, "zone", "wheel")
DH.change_data(color_message, "zone", "logo")
DH.change_data(color_message, "mode", "count")
DH.change_data(color_message["rate"], "frequency", "high")

DH.print_data(color_message, "color data: ")

# TODO try posting data for illumination control



# urllib experiment
# resolve port and host
PORT, plain_host = get_host(HOST, LOCAL_PORT)
print(plain_host)
host_port = "http://" + plain_host + ":" + str(PORT)
try:
    response_obj = urllib.request.urlopen(host_port, data=None, timeout=6.0)
except urllib.error.URLError as err:
    print("URLError: " + str(err.reason))
    # TODO handle error, refactor
    ResponseHandler.handle_error(ResponseHandler, err)

# print((response_obj.headers))
try:
    c_type = response_obj.headers["Content-Type"]
except:
    c_type = ""

# to string
response_str = str(response_obj.read(), 'utf-8')
print(response_str[0:min(len(response_str) - 1, 80)])

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
        save_name = "./data/response" + str(response_id) + file_type
        FH.save_data_file(FH, response_str, save_name)
        print("Saved ")

# taking screenshot of response
screenshot = TH.get_web_screen(host_port, DRIVER_PATH, "./data/screen.png")
print(screenshot)

# TODO find data sources
# Try interpreting predictions
if(HOST_ARGS[host_index] == "mi"):
    ResponseHandler.handle_prediction(response_str)

exit("\ndone")

##############################
# socket experiment
# print("HOST: " + plain_host)

# setup header
# broken:
accept_header = "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
# req_header = "GET / HTTP/1.0\r\nHost: 127.0.0.1\r\nAccept: text/plain\r\n"
# req_header = "GET / HTTP/1.0\r\nHost: {}\r\nAccept: {}\r\n".format(plain_host, accept_header)
# good header for localhost:
req_header = "GET / HTTP/1.0\r\nHost: 127.0.0.1\r\n\r\n"
# TODO general header
plain_host = HOST_LIST[0]# choose local host

# byte header
req_header_b = bytes(req_header, 'utf-8')
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
