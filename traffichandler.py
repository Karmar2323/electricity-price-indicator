# traffichandler.py
import urllib.request
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from responsehandler import ResponseHandler
# TODO Post to HTTP host

class TrafficHandler:
    def __init__(self) -> None:
        pass


    def init_request(address, data, method):
        #TODO check address
        if address.startswith("http"):
            address
        else:
            address = "http://" + address

        return TrafficHandler.make_request(address, data, method)


    def make_request(destination, data, method):
        # TODO

        try:
            response_obj = urllib.request.urlopen(destination, data=None, timeout=6.0)
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
    def get_web_screen(destination, cdriver_path, shot_name):

        options = Options()
        options.headless = True
        options.add_argument("--window-size=1024,768")

        driver = webdriver.Chrome(options=options, executable_path=cdriver_path)
        driver.get(destination)
        driver.save_screenshot(shot_name)
        driver.quit()

        return shot_name
