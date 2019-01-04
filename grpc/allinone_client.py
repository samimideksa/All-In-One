from __future__ import print_function
from io import BytesIO
from PIL import Image
from keras.models import model_from_json
from keras.models import Model
from scipy.io import loadmat
import os
import cv2 
import numpy as np
import pandas as pd
import dlib
#import .test.test_images as ti
from test import pre_calculated_faces
import grpc
from demo import load_model, selective_search_demo
from grpc.demo.main import images_demo, video_demo, process_video, webcam_demo, video_demo

import grpc.all_in_one_pb2
import grpc.all_in_one_pb2_grpc

import sys
import numpy as np


from grpc.all_in_one_pb2 import ImageRGB, BoundingBox, Point2D, FaceLandmarks, FaceDetections

image_data = None

def readinchunks(file_name, source_bboxes, chunk_size=1024*64):
    boxes = [BoundingBox(**b) for b in source_bboxes]
    header = grpc.all_in_one_pb2.FaceAlignmentHeader(
        source_bboxes=boxes,
    )

    yield grpc.all_in_one_pb2.FaceAlignmentRequest(header=header)

    with open(file_name, 'rb'):
        while True:
            chunk = grpc.infile.read(chunk_size)
            if chunk:
                yield grpc.all_in_one_pb2.FaceAlignmentRequest(image_chunk=ImageRGB(content=chunk))
            else:
                return

def align_face(stub, image_fn, source_bboxes):
    img_iterator = readinchunks(image_fn, source_bboxes)
    images = []
    image_data = None
    for data in stub.AlignFace(img_iterator):
        if data.HasField("header"):
            if image_data is not None:
                images.append(image_data)
            image_data = bytearray()
        else:
            image_data.extend(data.image_chunk.content)
    if image_data is not None:
        images.append(image_data)
    return images


def imagetopy(image, output_file):
    with open(image, 'rb') as fin:
        image_data = fin.read()

    with open(output_file, 'w') as fout:
        fout.write('image_data ='+ repr(image_data))

def pytoimage(pyfile):
    pymodule = __import__(pyfile)
    img = Image.open(BytesIO(pymodule.image_data))
    img.show()

def run():
    channel = grpc.insecure_channel('localhost:50051')
    stub = grpc.all_in_one_pb2_grpc.AllInOneStub(channel)

    #img_list_data = align_face(stub, r'test/test_images', source_bboxes=pre_calculated_faces['adele_2016.jpg'],)
    #for i in range(0, len(pre_calculated_faces['adele_2016.jpg'])):
    #    with open('test_align_%d.jpg' % i, 'wb') as f:
    #        f.write(img_list_data[i])

    response = stub.AllInOne(grpc.all_in_one_pb2.AllInOneRequest(image='Adele'))
    print("Greeter client received: " + str(response.gender))

if __name__ == '__main__':
    #imagetopy('adele_2016.jpg', 'decoded1.py')
    #pytoimage('decoded')
    model  = load_model("/home/samuel/projects/All-In-One/allinonemodels/allinone.json","/home/samuel/projects/All-In-One/allinonemodels/freeze2.h5",["age_estimation","smile", "gender_probablity"])
    model.summary()
    detector = dlib.get_frontal_face_detector()
    #image demo
    images_demo(model,"/home/samuel/projects/All-In-One/grpc/test/test_images/",detector)
    #video demo
    #webcam_demo(model,detector)
    video_demo(model,"/home/samuel/projects/All-In-One/grpc/test/test_videos/video_demo3.mp4",detector)
    #selective_search_demo()
    run()   
    
