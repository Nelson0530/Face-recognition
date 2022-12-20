import cv2
import numpy as np
import face_recognition
from time import time
import Getencode
from T_NewUserAndencode import User

classNames, encodeListKnown = Getencode.getencoding()

cap = cv2.VideoCapture(0)
start_time = time()
name = ''
while True:
    sucess, img = cap.read()
    cv2.imshow('WebCam', img)
    end_time = time()
    process_time = end_time - start_time
    cv2.waitKey(1)
    if process_time > 3:
        imgS = cv2.resize(img, (0, 0), None, fx=0.25, fy=0.25)  # resize img to improve matching process in furture
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)  # get ready to get encoding from face_recognition module
        faceCurFrame = face_recognition.face_locations(imgS)  # find all faces' location in pic
        encodesCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)  # encoding imgS from facesCurFrame(all faces' Loc.)
        # Start matching
        for encodeFace, faceLoc in zip(encodesCurFrame, faceCurFrame):  # get encodeFace from encodesCurFrame and get faceLoc in facesCurFrame in same loop
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace, tolerance=0.45)  # give tolerance to avoid error detection
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
            print(faceDis)
            matchIndex = np.argmin(faceDis)  # return the index of lowest distance(value) in faceDis list
            # Display match result rect and write the match name
            if matches[matchIndex]:  # return True or False from matches list's element which have lowest distance
                name = classNames[matchIndex].upper()
                y1, x2, y2, x1 = faceLoc  # we load location from imgS (scaled image!)
                y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4 # locations need to be compensated with scale!
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.rectangle(img, (x1, y2-35), (x2, y2), (0, 255, 0), cv2.FILLED)
                cv2.putText(img, name, (x1+6, y2-6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
                cv2.imshow('WebCam', img)
                cv2.waitKey(0)

                break
            else:
                break
        cv2.waitKey(0)
        break
print(name)        

if name:
    print(f'Welcome Back! {name}!')
else:
    print(f'Hey! New Guy! Let\'s get started!')
    Newuser = User()
    Result = Newuser.NewUser()
    Newuser.markAttendance(Result)

cap.release()
cv2.destroyAllWindows()
