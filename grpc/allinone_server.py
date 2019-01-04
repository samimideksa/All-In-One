from concurrent import futures
import time
import grpc
from keras.models import model_from_json
from keras.models import Model
from scipy.io import loadmat
import os
import cv2 
import numpy as np
import pandas as pd
import dlib
from grpc.all_in_one_pb2 import all_in_one_pb2
from grpc import all_in_one_pb2_grpc
from demo import load_model, selective_search_demo
from grpc.demo.main import images_demo, video_demo, process_video, webcam_demo, video_demo
import sys
_ONE_DAY_IN_SECONDS = 60 * 60 * 24

class Greeter(all_in_one_pb2_grpc.AllInOneServicer):
    def SayHello(self, request, context):
        return all_in_one_pb2.AllInOneResponse(message="Hello, %s" % request.name)

    def AllInOne(self, request, context):
        return all_in_one_pb2.AllInOneResponse()

class Server():
    def __init__(self):
        self.port = '[::]:50051'
        self.server = None

    def start_server(self):
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        all_in_one_pb2_grpc.add_AllInOneServicer_to_server(Greeter(), self.server)
        print('Starting server. Listening on port 50051')
        self.server.add_insecure_port(self.port)
        self.server.start()
        model  = load_model("/home/samuel/projects/All-In-One/allinonemodels/allinone.json","/home/samuel/projects/All-In-One/allinonemodels/freeze2.h5",["age_estimation","smile", "gender_probablity"])
        model.summary()
        detector = dlib.get_frontal_face_detector()
        #image demo
        images_demo(model,"/home/samuel/projects/All-In-One/grpc/test/test_images/",detector)
        #video demo
        #webcam_demo(model,detector)
        video_demo(model,"/home/samuel/projects/All-In-One/grpc/test/test_videos/video_demo3.mp4",detector)
        try:
            while True:
                time.sleep(_ONE_DAY_IN_SECONDS)
        except KeyboardInterrupt:
            self.server.stop(0)
        
        def stop_server(self):
            self.server.stop(0)

# def serve():
#     server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
#     all_in_one_pb2_grpc.add_AllInOneServicer_to_server(Greeter(), server)
#     server.add_insecure_port('[::]:50051')
#     server.start()
#     model  = load_model("/home/samuel/projects/All-In-One/allinonemodels/allinone.json","/home/samuel/projects/All-In-One/allinonemodels/freeze2.h5",["age_estimation","smile", "gender_probablity"])
#     model.summary()
#     detector = dlib.get_frontal_face_detector()
#     #image demo
#     images_demo(model,"/home/samuel/projects/All-In-One/grpc/test/test_images/",detector)
#     #video demo
#     #webcam_demo(model,detector)
#     video_demo(model,"/home/samuel/projects/All-In-One/grpc/test/test_videos/video_demo3.mp4",detector)
#     try:
#         while True:
#             time.sleep(_ONE_DAY_IN_SECONDS)
#     except KeyboardInterrupt:
#         server.stop(0)

if __name__ == '__main__':
    model  = load_model("/home/samuel/projects/All-In-One/allinonemodels/allinone.json","/home/samuel/projects/All-In-One/allinonemodels/freeze2.h5",["age_estimation","smile", "gender_probablity"])
    model.summary()
    detector = dlib.get_frontal_face_detector()
    #image demo
    images_demo(model,"/home/samuel/projects/All-In-One/grpc/test/test_images/",detector)
    #video demo
    #webcam_demo(model,detector)
    video_demo(model,"/home/samuel/projects/All-In-One/grpc/test/test_videos/video_demo3.mp4",detector)
    Server.start_server()
