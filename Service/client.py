import grpc

import detect_image_pb2
import detect_image_pb2_grpc    
# Open a grpc channel
from PIL import Image
import sys

class ClientTest():
    def __init__(self,port='localhost:50051',image_output='client_out'):
	    self.port = port
	    self.image_output = image_output
    def open_grpc_channel(self):
        channel = grpc.insecure_channel(self.port)
        stub = detect_image_pb2_grpc.ImageDemoStub(channel)
        return stub
    def send_request(self, stub, img):
        out_file_name = self.image_output+'.png'
        img = img
        img = img.resize((480,320))
        img_b = img.tobytes()     
        Image = detect_image_pb2.InputImage(Image =img_b)
        response = stub.DetectImage(Image)
        image = Image.frombytes(data=response.Image,size=(480,320),mode='RGB')
        return image

#make the call 

# print(type(response.Image))

