from tkinter import*
from PIL import Image,ImageTk
from tkinter import ttk
from tkinter import messagebox
import mysql.connector
from student import Student
import cv2
import os
import numpy as np
from time import strftime
from datetime import datetime

class Face_Recognition:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1500x790+0+0")
        self.root.title("Face recognition system")
        
        title_lbl=Label(self.root,text="FACE RECOGNITION",font=("times new roman",35,"bold"),bg="white",fg="green")
        title_lbl.place(x=-90,y=0,width=1500,height=45)
        #1st img
        img_top=Image.open("img/facerec.jpg")
        img_top=img_top.resize((650,700),Image.ADAPTIVE)
        self.photoimg_top=ImageTk.PhotoImage(img_top)

        f_lbl=Label(self.root,image=self.photoimg_top)
        f_lbl.place(x=0,y=55,width=650,height=700)
        #2nd img
        img_bottom=Image.open("img/facialrec.png")
        img_bottom=img_bottom.resize((950,700),Image.ADAPTIVE)
        self.photoimg_bottom=ImageTk.PhotoImage(img_bottom)

        f_lbl=Label(self.root,image=self.photoimg_bottom)
        f_lbl.place(x=650,y=55,width=950,height=700)

        #button
        b1_1=Button(f_lbl,text="Face Recognition",cursor="hand2",command=self.face_recog,font=("times new roman",18,"bold"),bg="green",fg="white")
        b1_1.place(x=350,y=550,width=200,height=40)
        
        
    def mark_attendance(self,r,n,a):
        with open("attend.csv","r+",newline="\n") as f:
            myDataList=f.readlines()
            name_list=[]
            for line in myDataList:
                entry=line.split((","))
                name_list.append(entry[0])
            if((r not in name_list) and (n not in name_list) and (a not in name_list)):
                now=datetime.now()
                d1=now.strftime("%d/%m %y")
                dtString=now.strftime("%H:%M:%S")
                f.writelines(f"\n{r},{n},{a},{dtString},{d1},present")
        
    #====face recognition===========     
    def face_recog(self):
        def draw_boundary(img,classifier,scaleFactor,minNeighbors,color,text,clf):
            gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            features = classifier.detectMultiScale(gray_image, scaleFactor, minNeighbors)
            #coord=[]
            coords=[]

            for (x, y, w, h) in features:
                cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0) , 3)
                id,predict=clf.predict(gray_image[y:y+h, x:x+w])
                confidence=int((100*(1-predict/300)))

                conn = mysql.connector.connect(host="localhost",user="root",password="",database="student_db")
                my_cursor = conn.cursor()
                my_cursor.execute("select std_roll from student where std_id="+ str(id)) 
                r=my_cursor.fetchone()
                r='+'.join(map(str,r))

                my_cursor.execute("select std_name from student where std_id="+ str(id))
                n=my_cursor.fetchone()
                n='+'.join(map(str,n))

                my_cursor.execute("select std_address from student where std_id="+ str(id))
                a=my_cursor.fetchone()
                a='+'.join(map(str,a))

                #my_cursor.execute("select Id from student where Id"+str(id))
                #i=my_cursor.fetchone()
                # i="+".join(map(str,i))
            
                if confidence>77:
                  #  cv2.putText(img,f"Id:{i}",(x,y-75),cv2.FONT_HERSHEY_COMPLEX,0.8,(255,255,255),3)
                    cv2.putText(img,f"Confidence:{confidence}%",(x,y-90),cv2.FONT_HERSHEY_COMPLEX,0.8,(255,255,255),3)
                    cv2.putText(img,f"std_roll:{r}",(x,y-55),cv2.FONT_HERSHEY_COMPLEX,0.8,(255,255,255),3)
                    cv2.putText(img,f"std_name:{n}",(x,y-30),cv2.FONT_HERSHEY_COMPLEX,0.8,(255,255,255),3)
                    cv2.putText(img,f"std_address:{a}",(x,y-5),cv2.FONT_HERSHEY_COMPLEX,0.8,(255,255,255),3)
                    self.mark_attendance(r,n,a)
                else:
                    cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),3)
                    cv2.putText(img,"unknown Face",(x,y-5),cv2.FONT_HERSHEY_COMPLEX,0.8,(255,255,255),3)
                    #self.mark_attendance(r,n,a)
                coords=[x,y,w,y]
        
            return coords

        def recognize(img,clf,faceCascade):
             coords= draw_boundary(img,faceCascade,1.1,10,(255,25,255),"Face",clf)
             return img
        

        faceCascade=cv2.CascadeClassifier("my_venv/Lib/site-packages/cv2/data/haarcascade_frontalface_default.xml")
        clf = cv2.face.LBPHFaceRecognizer_create()
        clf.read("classifier.xml")

        video_cap=cv2.VideoCapture(0)

        while True:
            ret,img = video_cap.read()
            img=recognize(img,clf,faceCascade) 
            cv2.imshow("welcome to Face Recognition",img)
            
            if cv2.waitKey(1)==13:
              break
        video_cap.release()
        cv2.destroyAllWindows()


        
        
if __name__ == "__main__":
    root = Tk()
    obj = Face_Recognition(root)
    root.mainloop()
