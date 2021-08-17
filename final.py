import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
from datetime import date
from tkinter import *
from PIL import Image, ImageTk
from tkinter.filedialog import askopenfile
import gspread
import webbrowser
from oauth2client.service_account import ServiceAccountCredentials


today = date.today()
dtstring = today.strftime('%d-%m-%y')





def exam():
    U.set("Loading......")
    webbrowser.open('https://docs.google.com/spreadsheets/d/1agveM58jlnOtKziW2fDa-HzDIEKPk7GP-1PdSxzUC6I/edit#gid=0')
    U.set("View Attendance")
    return
def gone():
    file = open("C:\\CAPSTONE PROJECT CODE\\capstone project\\table.csv", "r+")
    file.truncate(0)
    file.close()

def findEncodings(images):
   encodeList = []
   for img in images:
       img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
       encode = face_recognition.face_encodings(img)[0]
       encodeList.append(encode)
   return encodeList

path = 'C:\\CAPSTONE PROJECT CODE\\capstone project\\student list'
images = []
classNames = []
myList = os.listdir(path)
print(myList)
curImg = []
for cl in myList:
   curImg = cv2.imread(f'{path}/{cl}')
   images.append(curImg)
   classNames.append(os.path.splitext(cl)[0])
print(classNames)
encodeListknown = findEncodings(images)
print('encoding complete')

def exa():
    T.set("loading.....")
    file = askopenfile(parent=vishal, mode='r+', title = "ADD DATA",filetype=[("Jpg file","*.jpg"),("ALL FILES", "*.*")])
    if file:

     print("its working")
    T.set("Browse and add image")



    return

def markattendance(name):

    with open('C:\\CAPSTONE PROJECT CODE\\capstone project\\table.csv', 'r+') as f:
        myDataList = f.readlines()
        nameList = []
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
        if name not in nameList:
           today = date.today()
           now = datetime.now()

           tstring = now.strftime('%I:%M:%S:%p')
           dtstring = today.strftime('%d-%m-%y')
           f.writelines(f'\n{name},{tstring},{dtstring}')

           pandu = []
           pandu.append(name)
           pandu.append(tstring)
           pandu.append(dtstring)
           scope = ['https://www.googleapis.com/auth/drive']

           creds = ServiceAccountCredentials.from_json_keyfile_name("C:\\CAPSTONE PROJECT CODE\\capstone project\\vishal.json", scope)

           client = gspread.authorize(creds)

           sheet = client.open("tutorial").sheet1  # Open the spreadhseet
           sheet.insert_row(pandu, 3)





def Take():
 gone()


 cap = cv2.VideoCapture(0)
 cap.set(3,1000)
 cap.set(4,1000)
 flag = 1

 while True:
    success, img = cap.read()
    imgs = cv2.resize(img, (0,0), None, 0.25,0.25)
    imgs = cv2.cvtColor(imgs, cv2.COLOR_BGR2RGB)

    facesCurFrame = face_recognition.face_locations(imgs)
    encodeCurFrame = face_recognition.face_encodings(imgs,facesCurFrame)

    for encodeFace,faceLoc in zip(encodeCurFrame,facesCurFrame):
        matches = face_recognition.compare_faces(encodeListknown,encodeFace)
        faceDis = face_recognition.face_distance(encodeListknown,encodeFace)
        #print(faceDis)
        matchIndex = np.argmin(faceDis)

        if matches[matchIndex]:
            name = classNames[matchIndex].upper()
            #print(name)
            y1,x2,y2,x1 = faceLoc
            y1, x2, y2, x1 = y1*4,x2*4,y2*4,x1*4
            cv2.rectangle(img,(x1,y1),(x2,y2),(0,0,255),2)
            cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,0,255),cv2.FILLED)
            cv2.putText(img,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,0,0),2)

            markattendance(name)



    cv2.imshow('webcam', img)


    if cv2.waitKey(10) & 0xFF == ord(' '):
        break
 cv2.destroyAllWindows()


vishal = Tk()
#vishal.call('wm', 'iconphoto', vishal._w, PhotoImage(file='face-recognition.png'))
vishal.iconbitmap('C:\\CAPSTONE PROJECT CODE\\capstone project\\face-recognition.ico')
vishal.geometry("1000x800")
vishal.title("Face recognition batch F4")
vishal.configure(bg='magenta')
a = Image.open("C:\\CAPSTONE PROJECT CODE\\capstone project\\Picture1.jpg")
a = a.resize((800,400))
b = ImageTk.PhotoImage(a)
c = Label(image=b)
c.pack()
Label(vishal,text="DATE: "+dtstring,font="italic 15 bold",relief=SUNKEN,borderwidth=10).pack(side=TOP,anchor='n')

S= StringVar()
T= StringVar()
U= StringVar()
T.set("Browse and add image")
U.set("View Attendance")


V = Button(vishal, textvariable=S, bg="blue", fg="brown", padx=50, pady=20, font="ITALIC 15 bold",
               borderwidth=5, relief=RIDGE,command=Take)
S.set("Take Attendance\n(press spacebar to exit frame)")
V.pack(side=BOTTOM,anchor='s',padx=5)
A = Button(vishal, textvariable=T, bg="pink", fg="blue", padx=50, pady=20, font="ITALIC 15 bold",
               borderwidth=5, relief=RIDGE,command=exa)
A.pack(side=BOTTOM,anchor="s",padx=5)
B = Button(vishal, textvariable=U, bg="black", fg="brown", padx=50, pady=20, font="ITALIC 15 bold",
               borderwidth=5, relief=RIDGE,command=exam)
B.pack(side=BOTTOM,anchor="s",padx=5)

vishal.mainloop()












