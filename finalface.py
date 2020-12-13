import cv2
import numpy as np
import face_recognition
import os
import datetime

path = 'images'
pathTo = 'unauthorised'
images = []
names = []
myList = os.listdir(path)
print(myList)

for name in myList:
	curImg = cv2.imread(f'{path}/{name}')
	images.append(curImg)
	names.append(os.path.splitext(name)[0])

print(names)

def findEncodings(images):
	encodeList = []
	for img in images:
		img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
		encode = face_recognition.face_encodings(img)[0]
		encodeList.append(encode)
	return encodeList

encodeListKnown = findEncodings(images)
print('Encoding Complete')

cap = cv2.VideoCapture(0)
unknown = 0							#flag for capturing new faces

while True:
	success, img = cap.read()
	imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
	imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

	facesCurFrame = face_recognition.face_locations(imgS)
	encodeCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

	for encodeFace, faceLoc, in zip(encodeCurFrame, facesCurFrame):
		matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
		faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
		matchIndex = np.argmin(faceDis)
		#print(matches)

		if matches.count(matches[0]) == len(matches):
			unknown+=1
			encodeListKnown.append(encodeFace)
			names.append("unknown"+str(unknown))
			dtString = datetime.datetime.now().strftime('%H:%M:%S')
			Y1, X2, Y2, X1 = faceLoc
			#Y1, X2, Y2, X1 = Y1*4, X2*4, Y2*4, X1*4
			crop = imgS[Y1:Y2, X1:X2]
			cv2.imwrite(f'{pathTo}/{names[-1]+" "+dtString+".jpg"}', cv2.resize(cv2.cvtColor(crop, cv2.COLOR_BGR2RGB), (0, 0), None, 4, 4))


		if matches[matchIndex]:
			name = names[matchIndex].upper()
			#print(name)
			y1, x2, y2, x1 = faceLoc
			y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
			cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
			cv2.rectangle(img, (x1, y2-35), (x2, y2), (0, 255, 0), cv2.FILLED)
			cv2.putText(img, name, (x1+6, y2-6), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
			# (str(x1)+", "+str(y1)+"\n"+str(x2)+", "+str(y2))

	encode = face_recognition.face_encodings(imgS)

	cv2.imshow('Webcam', img)
	key = cv2.waitKey(1)
	if key == ord('p'):
		break
cap.release()