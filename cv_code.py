
from db_interface import add_attendence, get_name


import cv2
import numpy as np
import face_recognition


def findEncodings(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    encode = face_recognition.face_encodings(img)
    return encode

def get_embedding(wait=30):
    cap = cv2.VideoCapture(0)
    k = 0
    while True:
        k += 1
        _ , img = cap.read()
        imgS = cv2.resize(img,(0,0),None,0.25,0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
        facesCurFrame = face_recognition.face_locations(imgS)

        if k == wait:
            enc = findEncodings(img)
            break
        
        if facesCurFrame:
            for faceLoc in facesCurFrame:
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.imshow('Webcam', img)
        cv2.waitKey(1)


    cap.release()
    cv2.destroyAllWindows()
    return enc[0]


listed_student_ids = []
def monitor(cnx, cursor, embeddings):

    IDs = [i['id'] for i in embeddings]
    encodeListKnown = [i['embeddings'] for i in embeddings]
    
    cap = cv2.VideoCapture(0)
    
    while True:
        _, img = cap.read()

        imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
        
        facesCurFrame = face_recognition.face_locations(imgS)
        encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)
        
        for encodeFace,faceLoc in zip(encodesCurFrame, facesCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)

            matchIndex = np.argmin(faceDis)
            if matches[matchIndex]:
                student_id = IDs[matchIndex]
                name = get_name(cnx, cursor, student_id)
                
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
                if student_id not in listed_student_ids:
                    listed_student_ids.append(student_id)
                    print("Detected Student:", name)
                    add_attendence(cnx, cursor, student_id)
        
        cv2.imshow('Webcam', img)
        key = cv2.waitKey(1)
        if key == 27:
            break
    cap.release()
    cv2.destroyAllWindows()