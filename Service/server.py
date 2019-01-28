import grpc
from concurrent import futures
import time

#import the generated classes
import detect_image_pb2
import detect_image_pb2_grpc
import detect

class ImageDemoServicer(detect_image_pb2_grpc.ImageDemoServicer):
# detect.images_demo is exposed here
  def DetectImage(self, request, context):
      response = detect_image_pb2.OutputImage()
      response.Image = detect.images_demo(response.Image)
      return response

class Server():
    def __init__(self):
        self.port = '[::]:50051'
        self.server = None
    def start_server(self):
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        detect_image_pb2_grpc.add_ImageDemoServicer_to_server(ImageDemoServicer(), self.server)
        print('Starting server. Listening on port 50051.')
        self.server.add_insecure_port(self.port)
        self.server.start()        
    def stop_server(self):
        self.server.stop(0)

