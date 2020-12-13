import tkinter as tk
import tkinter as ttk
import cv2
from PIL import Image, ImageTk
import os
import datetime
import face_recognition
import numpy as np 
import platform
import subprocess


path = 'images'
pathTo = 'unauthorised'
images = []
names = []
myList = os.listdir(path)
print(myList)
unknown = 0

for name in myList:                                     #simply reads file names to identify faces
    curImg = cv2.imread(f'{path}/{name}')
    images.append(curImg)
    names.append(os.path.splitext(name)[0])

print(names)

def findEncodings(images):                              #finding facial encodings
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

encodeListKnown = findEncodings(images)
print('Encoding Complete')


FNT= ("Verdana", 18)
LRG_FNT = ("Verdana", 25)
#caps = cv2.VideoCapture(0)


class caps(tk.Tk):

    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand = True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, PageOne, PageTwo, about, helpp, face):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()

        
class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="Security App", font=LRG_FNT)
        label.pack(pady=10,padx=10)

        button = tk.Button(self, text="Activate",
                            command=lambda: controller.show_frame(face))
        button.pack(pady = 10, padx = 10)

        button1 = tk.Button(self, text="Add Users",
                            command=lambda: controller.show_frame(PageOne))
        button1.pack(pady = 10, padx = 10)

        button2 = tk.Button(self, text="Settings",
                            command=lambda: controller.show_frame(PageTwo))
        button2.pack(pady = 10, padx = 10)


class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, font=LRG_FNT)
        label.pack(pady=10,padx=10)
        label['text'] = "Add Users"

        imageFrame = tk.Frame(self, width=100, height=100)
        imageFrame.pack(pady = 10, padx = 10)#grid(row=0, column=0, padx=10, pady=2)
        #b = tk.Button(window, text = "yeet", command = show_frame)
        #b.pack(pady = 10, padx = 10)#grid(row=1, column=0, padx=10, pady=2)

        L = tk.Label(self, text="enter your name", font=FNT)
        L.pack(pady=10,padx=10)

        name = tk.Entry(self, font=FNT)
        name.insert(0, "name")
        name.pack(pady=10,padx=10)

        #Capture video frames
        lmain = tk.Label(imageFrame)
        lmain.pack(pady = 10, padx = 10)#grid(row=0, column=0)
        cap = cv2.VideoCapture(0)

        def cam():
            _, frame = cap.read()
            frame = cv2.flip(frame, 1)
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            cv2image = cv2.resize(cv2image, (0, 0), None, 0.4, 0.4)
            img = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=img)
            lmain.imgtk = imgtk
            lmain.configure(image=imgtk)
            lmain.after(10, cam) 

        def pic():
            #global encodeListKnown
            _, frame = cap.read()
            frame = cv2.flip(frame, 1)

            #cv2.imshow('image', frame)
            imgS = cv2.resize(frame, (0, 0), None, 0.25, 0.25)
            imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
            facesCurFrame = face_recognition.face_locations(imgS)
            encodeCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

            for encodeFace, faceLoc, in zip(encodeCurFrame, facesCurFrame):
                matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
                faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)

            if matches.count(matches[0]) == len(matches):
                if names.count(name.get()) == 0:
                    print("put er in")
                    img = cv2.resize(imgS, (0, 0), None, 4, 4)
                    #cv2.imshow('test', img)
                    image = Image.fromarray(img)
                    print (name.get())
                    fname = path+"/"+name.get()+".jpg"
                    image.save(fname)
                    encodeListKnown.append(face_recognition.face_encodings(img)[0])
                    names.append(name.get())
                    print('Encoding Complete')
                else:
                    print("choose a different name")                    #error message for repeated name
                    win.wm_title("error")
                    #win.geometry("100x100")

                    l = tk.Label(win, text="choose a different name")
                    l.grid(row=0, column=0)

                    b = ttk.Button(win, text="Okay", command=win.destroy)
                    b.grid(row=1, column=0) 
            else:
                print("encoding already exists")                        #error message for repeated face
                win = tk.Toplevel()
                win.wm_title("error")
                #win.geometry("100x100")

                l = tk.Label(win, text="encoding already exists")
                l.grid(row=0, column=0)

                b = ttk.Button(win, text="Okay", command=win.destroy)
                b.grid(row=1, column=0)         
        #print(matches)

        button1 = tk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack(pady = 10, padx = 10)

        bp = tk.Button(self, text="Add User",
                            command=pic)
        bp.pack(pady = 10, padx = 10)

        cam()



class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Settings", font=LRG_FNT)
        label.pack(pady=10,padx=10)

        button1 = tk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack(pady = 10, padx = 10)

        button2 = tk.Button(self, text="About",
                            command=lambda: controller.show_frame(about))
        button2.pack(pady = 10, padx = 10)

        button3 = tk.Button(self, text="Help",
                            command=lambda: controller.show_frame(helpp))
        button3.pack(pady = 10, padx = 10)

        def ba():
            if platform.system() == "Windows":
                os.startfile(path)
            elif platform.system() == "Darwin":
                subprocess.Popen(["open", path])
            else:
                subprocess.Popen(["xdg-open", path])

        def bu():
            if platform.system() == "Windows":
                os.startfile(pathTo)
            elif platform.system() == "Darwin":
                subprocess.Popen(["open", pathTo])
            else:
                subprocess.Popen(["xdg-open", pathTo])


        ba = tk.Button(self, text = "Browse Authorised",
                            command = ba)
        ba.pack(pady = 10, padx = 10)

        bu = tk.Button(self, text = "Browse Unauthorised",
                            command = bu)
        bu.pack(pady = 10, padx = 10)



class about(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        f = open("about.txt", "r")
        label = tk.Label(self, text = f.read(), font=FNT)
        label.pack(pady=10,padx=10)

        button = tk.Button(self, text="Back to Settings",
                            command=lambda:controller.show_frame(PageTwo))
        button.pack(pady = 10, padx = 10)


class helpp(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text = "put in instructions text", font=FNT)
        label.pack(pady=10,padx=10)

        button = tk.Button(self, text="Back to Settings",
                            command=lambda:controller.show_frame(PageTwo))
        button.pack(pady = 10, padx = 10)
        
class face(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text = "Face Detection", font=LRG_FNT)
        label.pack(pady=10,padx=10)

        imageFrame = tk.Frame(self, width=100, height=100)
        imageFrame.pack(pady = 10, padx = 10)#grid(row=0, column=0, padx=10, pady=2)
        #b = tk.Button(window, text = "yeet", command = show_frame)
        #b.pack(pady = 10, padx = 10)#grid(row=1, column=0, padx=10, pady=2)

        #Capture video frames
        lmain = tk.Label(imageFrame)
        lmain.pack(pady = 10, padx = 10)#grid(row=0, column=0)

        cap = cv2.VideoCapture(0)

        def activate():
            global unknown
            label['text'] = "Face Detection Active"
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
                    print(name)
                    y1, x2, y2, x1 = faceLoc
                    y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
                    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.rectangle(img, (x1, y2-35), (x2, y2), (0, 255, 0), cv2.FILLED)
                    cv2.putText(img, name, (x1+6, y2-6), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                    # (str(x1)+", "+str(y1)+"\n"+str(x2)+", "+str(y2))

            encode = face_recognition.face_encodings(imgS)
            lmain.after(10, activate)


        ba = tk.Button(self, text ="Activate",
                            command=activate)
        ba.pack(pady = 10, padx = 10)

        button = tk.Button(self, text="Deactivate",
                            command=lambda:controller.show_frame(StartPage))
        button.pack(pady = 10, padx = 10)


app = caps()
#app.geometry("720x480")
app.title("Capstone / CyberSecurity Project")
app.mainloop()