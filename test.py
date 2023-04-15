import unittest
from traffichandler import TrafficHandler as TH
from filehandler import FileHandler as FH

class TestMethods(unittest.TestCase):
    def test_init_request(self):
        color_json = FH.read_file(FH, "colordata.json")
        
        addr, data, method = TH.init_request(TH, '127.0.0.1:3001', color_json, "POST")
        self.assertTrue(type(data) == "buffer")


if __name__ == '__main__':
    unittest.main()