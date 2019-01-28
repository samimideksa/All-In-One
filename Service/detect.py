import sys
sys.path.append('..')
from demo.__main__ import get_cmd_args, images_demo
from PIL import Image
import os
import cv2
import numpy as np


def images_demo(model,img_bytes,detector):

    for imgfile in os.listdir(img_bytes):
        # TODO image = IMGBYTE.convert to image
        # image = cv2.imread(os.path.join(images_dir,imgfile))
        print (image.shape)
        faces = detector(image)
        for i in range(len(faces)):
            face = faces[i]
            face_image = image[face.top():face.bottom(),face.left():face.right()]
            face_image = cv2.resize(face_image,(227,227))
            face_image = face_image.astype(np.float32)/255
            predictions = model.predict(face_image.reshape(-1,227,227,3))
            image = cv2.rectangle(image, (face.left(),face.top()), (face.right(),face.bottom()), (255,0,0),thickness=3)
            age_estimation = predictions[0][0]
            smile_detection = predictions[1][0]
            gender_probablity = predictions[2][0]

            age = str(int(age_estimation))
            smile = np.argmax(smile_detection)
            gender = np.argmax(gender_probablity)

            if(smile==0):
                smile = "False"
            else:
                smile = "True"
            if(gender == 0):
                gender= "Female"
            else:
                gender = "Male"

            cv2.putText(image, "Age: "+age, (face.left() + 10, face.top() + 10), cv2.FONT_HERSHEY_DUPLEX, 0.4,
                    (255,0,0))
            cv2.putText(image, "Smile: "+smile, (face.left() + 10, face.top() + 20), cv2.FONT_HERSHEY_DUPLEX, 0.4,(255,0,0))
            cv2.putText(image, "Gender: "+gender, (face.left() + 10, face.top() + 30), cv2.FONT_HERSHEY_DUPLEX, 0.4,
                    (255,0,0))
        cv2.imshow("image",image)
        cv2.imwrite('adele.png',image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        
        return image

images_demo()