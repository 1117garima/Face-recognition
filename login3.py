from tkinter import*
from tkinter import ttk, messagebox
import tkinter as tk
from PIL import Image,ImageTk
from register import Register
#from login import Login_Window
from main import Face_Recognition_System
import mysql.connector
from student import Student
from train import Train
from face_recognition import Face_Recognition
from attendance import Attendances
import os
import re

def main():
    win=Tk()
    app=Login_Window(win)
    win.mainloop()

class Login_Window:
    def __init__(self,root):
        self.root=root
        self.root.title("Login")
        self.root.geometry("1500x800+0+0")

        # Session variable
        self.session = {}

        #variable
        self.admin_id=StringVar()
        self.admin_email=StringVar()
        self.admin_password=StringVar()
        
        def create_gradient(canvas, width, height, colors):
    # Create a gradient using a rectangle with a vertical linear gradient
            for i in range(height):
        # Interpolate between the two colors
              r = int(colors[0][0] * (height - i) / height + colors[1][0] * i / height)
              g = int(colors[0][1] * (height - i) / height + colors[1][1] * i / height)
              b = int(colors[0][2] * (height - i) / height + colors[1][2] * i / height)
              color = '#{:02x}{:02x}{:02x}'.format(r, g, b)
              canvas.create_line(0, i, width, i, fill=color, width=1)
    
        canvas = tk.Canvas(root, width=400, height=300)
        canvas.pack(fill=tk.BOTH, expand=True)
        
        start_color = (15, 16, 53) #white
        end_color = (54, 84, 134)     #blue
        create_gradient(canvas, 1500, 800, [start_color, end_color])
        #hover
        def onButton(event):
            loginbtn['bg']='#008DDA'
            loginbtn['fg']='#00008B'
        def onregbutton(event):
            registerbtn['bg']='#008DDA'
            registerbtn['fg']='#00008B'
              
        def leaveButton(event):
            loginbtn['bg']='#7FC7D9'
            loginbtn['fg']='white'
        def leaveregbutton(event):
            registerbtn['bg']='#7FC7D9'
            registerbtn['fg']='white'
            
        ##Background image
        #root.config(bg="#161616")
       # self.bg=ImageTk.PhotoImage(file=r"img/faced.jpg")
        
       # lbl_bg = Label(self.root,image=self.bg)
       # lbl_bg.place(x=0,y=0,relwidth=1,relheight=1)
        
        frame=Frame(self.root,bd=4,relief=RAISED,bg="#40679E")
        frame.place(x=230,y=110,width=850,height=490)
        

        
        ##image
        

        #f_lbl = Label(self.root,image=self.photoimg)
        #f_lbl.place(x=670,y=170,width=100,height=90)

       

        get_str=Label(frame,text="Login", font=("Victoria",45,"bold"),fg="#7FC7D9", bg="#40679E")
        get_str.place(x=100,y=40)

        #label
        #adminid

        adminID_label= Label(frame,text= "Admin_ID",font=("times new roman",15,"bold"),fg="white",bg="#40679E")
        adminID_label.place(x=135,y=140)

        adminID_entry = ttk.Entry(frame,textvariable=self.admin_id,width=20,font=("times new roman",15,"bold"))
        adminID_entry.place(x=30,y=170,width=320)
        
        #username
        user_label=Label(frame,text="Email", font=("times new roman",15,"bold"),fg="white", bg="#40679E")
        user_label.place(x=150,y=215)

        email_entry=ttk.Entry(frame,textvariable=self.admin_email,width=20,font=("times new roman",15,"bold"))
        email_entry.place(x=30,y=245,width=320)

        #password
        password_label=Label(frame,text="Password", font=("times new roman",15,"bold"),fg="white", bg="#40679E")
        password_label.place(x=140,y=290)

        password_entry=ttk.Entry(frame,textvariable=self.admin_password,font=("times new roman",15,"bold"))
        password_entry.place(x=30,y=320,width=320)

        #LoginButton
        loginbtn=Button(frame,text="Login",command=self.login,font=("times new roman",15,"bold"),bd=2, relief=RIDGE,fg="white",bg="#7FC7D9",activeforeground="#008DDA",activebackground="#7FC7D9")
        loginbtn.place(x=30,y=400,width=140,height=35)
        loginbtn.bind('<Enter>',onButton)
        loginbtn.bind('<Leave>',leaveButton)
        #RegisterButton
        
        registerbtn=Button(frame,text="Admin Register",command=self.register_window,font=("times new roman",14,"bold"),bd=2, relief=RIDGE,fg="white",bg="#7FC7D9",activeforeground="#008DDA",activebackground="#7FC7D9")
        registerbtn.place(x=190,y=400,width=170,height=35)
        registerbtn.bind('<Enter>',onregbutton)
        registerbtn.bind('<Leave>',leaveregbutton)
        
        get_str1=Label(frame,text="Welcome To Face Recognition Attendance System", wraplength=300, font=("Tahoma",25,"bold"),fg="#F3D7CA", bg="#40679E")
        get_str1.place(x=500,y=170)
        #forgetpassbtn
        #forgetbtn=Button(frame,text="Forget Password",font=("times new roman",12,"bold"),borderwidth=0, relief=RIDGE,fg="green",bg="lightblue",activeforeground="green",activebackground="lightblue")
        #forgetbtn.place(x=30,y=370,width=165)
    def register_window(self):
        # Hide the login window
        self.root.withdraw()

        # Open the registration window and pass the login window reference
        self.new_window = Toplevel()
        self.app = Register(self.new_window, self.root)



    def login(self):
        if self.admin_email.get() == "" or self.admin_password.get() == "":
            messagebox.showerror("Error", "All fields required", parent=self.root)
        else:
            try:
                conn = mysql.connector.connect(host="localhost", user="root", passwd="", database="student_db")
                my_cursor = conn.cursor()
                my_cursor.execute("select * from useradmin where admin_email=%s and admin_password=%s", (
                    #self.admin_id.get(),  #changed
                    self.admin_email.get(),
                    self.admin_password.get()
                ))
                row = my_cursor.fetchone()
                if row is not None:
                    # Successfully logged in
                    #self.session['admin_id'] = row[0]  # Assuming admin_id is the first column in the useradmin table
                    self.session['admin_email'] = row[4]  # Assuming admin_username is the second column
                    self.session['admin_password'] = row[7]
                    self.root.destroy()  # Close login window
                    self.open_main_page()  # Open main page
                else:
                    messagebox.showerror("Error", "Invalid id, email or password", parent=self.root)
                conn.close()
            except Exception as e:
                messagebox.showerror("Error", f"Error: {str(e)}", parent=self.root)

    def open_main_page(self):
        main_page_root = Tk()
        main_page = Face_Recognition_System(main_page_root)
        main_page_root.mainloop()


class Register:
    def __init__(self, root, login_window):
        self.root = root
        self.login_window = login_window  # Store the login window reference
        self.root.geometry("1530x790+0+0")
        self.root.title("Registration")

        # Variable
        self.admin_id = StringVar()
        self.admin_username = StringVar()
        self.admin_password = StringVar()
        self.admin_repassword = StringVar()
        self.admin_fullname = StringVar()
        self.admin_email = StringVar()
        self.admin_contact = StringVar()
        self.admin_address = StringVar()

        def create_gradient(canvas, width, height, colors):
        # Create a gradient using a rectangle with a vertical linear gradient
            for i in range(height):
        # Interpolate between the two colors
              r = int(colors[0][0] * (height - i) / height + colors[1][0] * i / height)
              g = int(colors[0][1] * (height - i) / height + colors[1][1] * i / height)
              b = int(colors[0][2] * (height - i) / height + colors[1][2] * i / height)
              color = '#{:02x}{:02x}{:02x}'.format(r, g, b)
              canvas.create_line(0, i, width, i, fill=color, width=1)
    
        canvas = tk.Canvas(root, width=400, height=300)
        canvas.pack(fill=tk.BOTH, expand=True)
        
        start_color = (15, 16, 53) #white
        end_color = (54, 84, 134)     #blue
        create_gradient(canvas, 1500, 800, [start_color, end_color])
        #hover
        def onregbutton(event):
            login_btn['bg']='#008DDA'
            login_btn['fg']='#00008B'
        def leaveregbutton(event):
            login_btn['bg']='#333A73'
            login_btn['fg']='white'
            
        
        ##Background image
        
      #  bg_img = Label(self.root,image=self.photoimg)
      #  bg_img.place(x=0,y=0,width=1530,height=790)

        f_frame=Frame(self.root,bd=0,relief=RIDGE,bg="#40679E")
        f_frame.place(x=200,y=100,width=900,height=500)


        #Register Label
        Register_label= Label(f_frame,text= "Register Here",font=("Victoria",30,"bold"),fg="#7FC7D9",bg="#40679E")
        Register_label.place(x=310,y=30)

         ##admin information
        frame = LabelFrame(root,bg="#40679E",fg="white", bd=0,relief=RIDGE,font=("times new roman",12,"bold"))
        frame.place(x=230,y=240,width=860,height=200)
        ##Admin ID
        admin_id= Label(frame,text= "Admin ID",font=("Victoria",15,"bold"),bg="#40679E",fg="white")
        admin_id.grid(row=0,column=0,padx=10,sticky=W,pady=10)
        
        adminID_entry = ttk.Entry(frame,textvariable=self.admin_id,width=30,font=("times new roman",12,"bold"))
        adminID_entry.grid(row=0,column=1,padx=10,sticky=W,pady=10,)
        
        #Admin Username
        username= Label(frame,text= "Username",font=("Victoria",15,"bold"),bg="#40679E",fg="white")
        username.grid(row=0,column=2,padx=10,pady=10,sticky=W)
        
        username_entry = ttk.Entry(frame,textvariable=self.admin_username,width=30,font=("times new roman",12,"bold"))
        username_entry.grid(row=0,column=3,padx=10,pady=10,sticky=W)
        ##Full name
        fullName= Label(frame,text= "FullName",font=("Victoria",15,"bold"),bg="#40679E",fg="white")
        fullName.grid(row=1,column=0,padx=10,pady=10,sticky=W)
        
        fullName_entry = ttk.Entry(frame,textvariable=self.admin_fullname,width=30,font=("times new roman",12,"bold"))
        fullName_entry.grid(row=1,column=1,padx=10,pady=10,sticky=W)
       
        ##contact
        contact= Label(frame,text= "Contact",font=("Victoria",15,"bold"),bg="#40679E",fg="white")
        contact.grid(row=1,column=2,padx=10,sticky=W)
        
        contact_entry = ttk.Entry(frame,textvariable=self.admin_contact,width=30,font=("times new roman",12,"bold"))
        contact_entry.grid(row=1,column=3,padx=10,sticky=W)

        #email
        email_label= Label(frame,text= "Email",font=("Victoria",15,"bold"),bg="#40679E",fg="white")
        email_label.grid(row=2,column=0,padx=10,sticky=W)
        
        email_entry = ttk.Entry(frame,textvariable=self.admin_email,width=30,font=("times new roman",12,"bold"))
        email_entry.grid(row=2,column=1,padx=10,sticky=W)

        ##address
        address_label= Label(frame,text= "Address",font=("Victoria",15,"bold"),bg="#40679E",fg="white")
        address_label.grid(row=2,column=2,padx=10,pady=10,sticky=W)
        
        address_entry = ttk.Entry(frame,textvariable=self.admin_address,width=30,font=("times new roman",12,"bold"))
        address_entry.grid(row=2,column=3,padx=10,pady=10,sticky=W)


         #password
        password_label= Label(frame,text= "Password",font=("Victoria",15,"bold"),bg="#40679E",fg="white")
        password_label.grid(row=3,column=0,padx=10,sticky=W)
        
        password_entry = ttk.Entry(frame,textvariable=self.admin_password,show="*",width=30,font=("times new roman",12,"bold"))
        password_entry.grid(row=3,column=1,padx=10,sticky=W)

        ##address
        repassword_label= Label(frame,text= "Retype Password",font=("Victoria",15,"bold"),bg="#40679E",fg="white")
        repassword_label.grid(row=3,column=2,padx=10,pady=10,sticky=W)
        
        repassword_entry = ttk.Entry(frame,textvariable=self.admin_repassword,show="*",width=30,font=("times new roman",12,"bold"))
        repassword_entry.grid(row=3,column=3,padx=10,pady=10,sticky=W)

        #Register button
        login_btn = Button(f_frame,text="Register",command=self.register,width=20,font=("times new roman",16,"bold"),bg="#333A73",fg="white")
        login_btn.place(x=325,y=385)
        login_btn.bind('<Enter>',onregbutton)
        login_btn.bind('<Leave>',leaveregbutton)

    def register(self):
        # Perform form validation
        if (not self.admin_username.get()) or (not self.admin_fullname.get()) or (not self.admin_contact.get()) or \
                (not self.admin_email.get()) or (not self.admin_address.get()) or (not self.admin_password.get()) or \
                (not self.admin_repassword.get()):
            messagebox.showerror("Error", "All fields are required")
            return

        if not self.admin_id.get().isdigit() or len(self.admin_id.get()) == 0:
            messagebox.showerror("Error", "Admin ID must be a numeric value")
            return

        if not isinstance(self.admin_username.get(), str) or not any(char.isalpha() for char in self.admin_username.get()):
            messagebox.showerror("Error", "Admin username must be a string value")
            return

        if not isinstance(self.admin_fullname.get(), str) or not re.match(r'^[a-zA-Z\s]+$', self.admin_fullname.get()):
            messagebox.showerror            ("Error", "Admin fullname must be a string value")
            return

        contact_pattern = r'^\d{10}$'  # Regular expression pattern for a 10-digit phone number
        if not re.match(contact_pattern, self.admin_contact.get()):
            messagebox.showerror("Error", "Invalid contact number")
            return

        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'  # Regular expression pattern for email
        if not re.match(email_pattern, self.admin_email.get()):
            messagebox.showerror("Error", "Invalid email address")
            return

        if not isinstance(self.admin_address.get(), str) or not re.match(r'^[a-zA-Z\s]+$', self.admin_address.get()):
            messagebox.showerror("Error", "Address must be a string value")
            return

        if self.admin_password.get() != self.admin_repassword.get():
            messagebox.showerror("Error", "Password and retype password must match")
            return

        try:
            # Connect to the database and insert the data
            conn = mysql.connector.connect(host="localhost", user="root", passwd="", database="student_db")
            my_cursor = conn.cursor()
            my_cursor.execute("INSERT INTO useradmin VALUES (%s,%s,%s,%s,%s,%s,%s,%s)", (
                self.admin_id.get(),
                self.admin_username.get(),
                self.admin_fullname.get(),
                self.admin_contact.get(),
                self.admin_email.get(),
                self.admin_address.get(),
                self.admin_password.get(),
                self.admin_repassword.get()
            ))
            conn.commit()
            conn.close()
             # Show success message
            messagebox.showinfo("Success", "Registered successfully")

                # Show the login window after successful registration
            self.login_window.deiconify()  # Show the login window again
            # Close the register window
            self.root.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Due to {str(e)}")




class Face_Recognition_System:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("Face Recognition System")

        # Main page GUI
        ##First image
        img = Image.open(r"img/download.jpg")
        img = img.resize((500, 130), Image.ADAPTIVE)
        self.photoimg=ImageTk.PhotoImage(img)

        f_lbl = Label(self.root,image=self.photoimg)
        f_lbl.place(x=0,y=0,width=500,height=130)

        ##second Image
        img1=Image.open(r"img/download.jpg")
        img1 = img1.resize((500,130),Image.ADAPTIVE)
        self.photoimg1=ImageTk.PhotoImage(img1)

        f_lbl = Label(self.root,image=self.photoimg1)
        f_lbl.place(x=500,y=0,width=500,height=130)

        ##3rd Image
        img2=Image.open(r"img/download.jpg")
        img2 = img2.resize((500,130),Image.ADAPTIVE)
        self.photoimg2=ImageTk.PhotoImage(img2)

        f_lbl = Label(self.root,image=self.photoimg2)
        f_lbl.place(x=1000,y=0,width=500,height=130)

        ##Background image
        img3=Image.open(r"img/bg.jpg")
        img3 = img3.resize((1530,790),Image.ADAPTIVE)
        self.photoimg3=ImageTk.PhotoImage(img3)

        bg_img = Label(self.root,image=self.photoimg3)
        bg_img.place(x=0,y=130,width=1530,height=790)
        
        title_lbl=Label(bg_img,text="Face Recognition Attendance System",font=("times new roman",35,"bold"),bg="white",fg="black")
        title_lbl.place(x=0,y=0,width=1530,height=50)

        ##student_button
        img4=Image.open(r"img/studentdetail.jpg")
        img4 = img4.resize((200,150),Image.ADAPTIVE)
        self.photoimg4=ImageTk.PhotoImage(img4)

        b1 = Button(bg_img,image=self.photoimg4,cursor="hand2",command=self.student_details)
        b1.place(x=250,y=100,width=200,height=150)

        b1_1 = Button(bg_img,text="Student Details",cursor="hand2",command=self.student_details,font=("times new roman",15,"bold"),bg="white",fg="black")
        b1_1.place(x=250,y=250,width=200,height=40)

        ##Detect_Face button
        img5=Image.open(r"img/facedet.jpg")
        img5 = img5.resize((200,150),Image.ADAPTIVE)
        self.photoimg5=ImageTk.PhotoImage(img5)

        b1 = Button(bg_img,image=self.photoimg5,cursor="hand2",command=self.face_data)
        b1.place(x=600,y=100,width=200,height=150)

        b1_1 = Button(bg_img,text="Face Detector",cursor="hand2",command=self.face_data,font=("times new roman",15,"bold"),bg="white",fg="black")
        b1_1.place(x=600,y=250,width=200,height=40)

        ##Attendance button
        img6=Image.open(r"img\Attendance.png")
        img6 = img6.resize((220,150),Image.ADAPTIVE)
        self.photoimg6=ImageTk.PhotoImage(img6)

        b1 = Button(bg_img,image=self.photoimg6,cursor="hand2",command=self.attendance)
        b1.place(x=950,y=100,width=200,height=150)

        b1_1 = Button(bg_img,text="Attendance",cursor="hand2",command=self.attendance,font=("times new roman",15,"bold"),bg="white",fg="black")
        b1_1.place(x=950,y=250,width=200,height=40)
        
     
        
        ##Train Face button
        img8=Image.open(r"img\facedetect.jpg")
        img8 = img8.resize((200,150),Image.ADAPTIVE)
        self.photoimg8=ImageTk.PhotoImage(img8)

        b1 = Button(bg_img,image=self.photoimg8,cursor="hand2",command=self.train_data)
        b1.place(x=250,y=350,width=200,height=150)

        b1_1 = Button(bg_img,text="Train Data",cursor="hand2",command=self.train_data,font=("times new roman",15,"bold"),bg="white",fg="black")
        b1_1.place(x=250,y=500,width=200,height=40)

        ##Photo Face button
        img9=Image.open(r"img\phot.png")
        img9 = img9.resize((200,150),Image.ADAPTIVE)
        self.photoimg9=ImageTk.PhotoImage(img9)

        b1 = Button(bg_img,image=self.photoimg9,cursor="hand2")
        b1.place(x=600,y=350,width=200,height=150)

        b1_1 = Button(bg_img,text="Photo",cursor="hand2",font=("times new roman",15,"bold"),bg="white",fg="black")
        b1_1.place(x=600,y=500,width=200,height=40)

    def open_img(self):
            os.startfile("data")      
        
        
 #===================Function buttons=================
       
    def student_details(self):
        self.new_window=Toplevel(self.root)
        self.app=Student(self.new_window)

    def train_data(self):
        self.new_window=Toplevel(self.root)
        self.app=Train(self.new_window)
        
    def face_data(self):
        self.new_window=Toplevel(self.root)
        self.app=Face_Recognition(self.new_window)
        
    def attendance(self):
        self.new_window=Toplevel(self.root)
        self.app=Attendances(self.new_window)

if __name__ == "__main__":
    #root = Tk()
    #obj = Login_Window(root)
    #root.mainloop()
    main()

