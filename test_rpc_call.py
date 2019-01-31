import sys
sys.path.insert(0, 'Service/')

from client import ClientTest
from server import *
from PIL import Image
import unittest
import numpy as np
import subprocess
import difflib

from all_in_one_pb2_grpc import AllInOneStub
from all_in_one_pb2 import AllInOneResponse, BoundingBox, AllInOneRequest

class TestSuiteGrpc(unittest.TestCase):
    def setUp(self):
       self.image = Image.open('Images/adele.png')
       self.server = Server()
       self.server.start_server()
       self.client = ClientTest()

    def test_grpc_call(self):
        stub = self.client.open_grpc_channel()
        result_image = self.client.send_request(stub, self.image)
        result_image = result_image.resize((480,320))
        result_image.save("Images/adele_predicted.png")
        img_res = np.asarray(Image.open("Images/adele_predicted.png").convert('L'))
        img_expected = np.asarray(Image.open("Images/adele_predicted.png")).convert('L')
        assert (img_res == img_expected).all()

if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(TestSuiteGrpc("test_grpc_call"))
    unittest.main()

