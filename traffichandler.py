# traffichandler.py
import urllib.parse
import urllib.request
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from responsehandler import ResponseHandler
# TODO Post to HTTP host

class TrafficHandler:
    def __init__(self) -> None:
        pass

    # Check and try to correct destination address. Prepare JSON data for posting.
    def init_request(self, address, data, method):
        # check address
        if address.startswith("http"):
            address
        else:
            address = "http://" + address

        if method == "POST":
            # TODO check data
            try:
                data = urllib.parse.urlencode(data)
            except TypeError:
                print("Can not parse data")
            # convert to buffer
            data = data.encode('utf-8')

        # return TrafficHandler.make_request(self, address, data, method)
        return(address, data, method)


    def make_request(self, destination, data, method):
        # TODO

        try:
            response_obj = urllib.request.Request(destination, data)
        except urllib.error.URLError as err:
            print("URLError: " + str(err.reason))
            # TODO handle error, refactor
            ResponseHandler.handle_error(ResponseHandler, err)
        return


# Get screenshot of web page using Selenium and Chromedriver as per the tutorial page
# IN: string destination,
#   string path to Chromedriver executable,
#   string name for screenshot
# OUT: string screenshot name
    def get_web_screen(self, destination, cdriver_path, shot_name):

        options = Options()
        options.headless = True
        options.add_argument("--window-size=1024,768")

        driver = webdriver.Chrome(options=options, executable_path=cdriver_path)
        driver.get(destination)
        driver.save_screenshot(shot_name)
        driver.quit()

        return shot_name
