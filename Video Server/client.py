import numpy
from pygame import mixer
import time
import cv2
from tkinter import *
import tkinter.messagebox

import socket
import struct
import time
import pickle
import imutils

root=Tk()
root.geometry('500x570')
frame = Frame(root, relief=RIDGE, borderwidth=2)
frame.pack(fill=BOTH,expand=1)
root.title('Virtual Theater')
frame.config(background='light blue')
label = Label(frame, text="Virtual Theater",bg='light blue',font=('Times 35 bold'))
label.pack(side=TOP)
filename = PhotoImage(file="./demo.png")
background_label = Label(frame,image=filename)
background_label.pack(side=TOP)



def hel():
   help(cv2)

def Contri():
   tkinter.messagebox.showinfo("Contributors","\n1.Saduni Wanasighe\n2.Yoshith Harshana \n3. Randika Viraj \n")


def anotherWin():
   tkinter.messagebox.showinfo("About",'Driver Cam version v1.0\n Made Using\n-OpenCV\n-Numpy\n-Tkinter\n In Python 3')
                                    
   

menu = Menu(root)
root.config(menu=menu)

subm1 = Menu(menu)
menu.add_cascade(label="Tools",menu=subm1)
subm1.add_command(label="Open CV Docs",command=hel)

subm2 = Menu(menu)
menu.add_cascade(label="About",menu=subm2)
subm2.add_command(label="Drivers",command=anotherWin)
subm2.add_command(label="Team",command=Contri)



def exitt():
   exit()

  
def open_cam():
   capture =cv2.VideoCapture(0)
   while True:
      ret,frame=capture.read()
      gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
      cv2.imshow('frame',frame)
      if cv2.waitKey(1) & 0xFF ==ord('q'):
         break
   capture.release()
   cv2.destroyAllWindows()
  

def stream_server():
   try:
      client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      client_socket.connect(('127.0.0.1', 8485))

      cam = cv2.VideoCapture(0)
      img_counter = 0

      #encode to jpeg format
      #encode param image quality 0 to 100. default:95
      #if you want to shrink data size, choose low image quality.
      encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),90]

      while True:
         ret, frame = cam.read()
         cv2.imshow('My Video',frame)
         frame = imutils.resize(frame, width=720)
         frame = cv2.flip(frame,180)
         result, image = cv2.imencode('.jpg', frame, encode_param)
         data = pickle.dumps(image, 0)
         size = len(data)

         if img_counter%10==0:
            client_socket.sendall(struct.pack(">L", size) + data)
            
         img_counter += 1
         
         if cv2.waitKey(1) & 0xFF == ord('q'):
            break
      client_socket.close()
      cam.release()
      cv2.destroyAllWindows()
   except:
     show_alert("Some thing goes wrong")
     alert()
   
   
   
def join_to_theater():
   conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   conn.connect(('127.0.0.1', 8080))

   data = b""
   payload_size = struct.calcsize(">L")
   print("payload_size: {}".format(payload_size))
   while True:
      while len(data) < payload_size:
         data += conn.recv(4096)
      # receive image row data form client socket
      packed_msg_size = data[:payload_size]
      data = data[payload_size:]
      msg_size = struct.unpack(">L", packed_msg_size)[0]
      while len(data) < msg_size:
         data += conn.recv(4096)
      frame_data = data[:msg_size]
      data = data[msg_size:]
      # unpack image using pickle 
      frame=pickle.loads(frame_data, fix_imports=True, encoding="bytes")
      frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)

      cv2.imshow('server',frame)
      if cv2.waitKey(1) & 0xFF == ord('q'):
            break
      cv2.waitKey(1)     
   cv2.destroyAllWindows()
   

def show_alert(msg):
   tkinter.messagebox.showinfo("Alert",msg)
   
def alert():
   mixer.init()
   alert=mixer.Sound('beep-07.wav')
   alert.play()
   time.sleep(0.1)
   alert.play()   
   


   
but1=Button(frame,padx=5,pady=5,width=39,bg='white',fg='black',relief=GROOVE,command=open_cam,text='Open Cam',font=('helvetica 15 bold'))
but1.place(x=5,y=176)


but3=Button(frame,padx=5,pady=5,width=39,bg='white',fg='black',relief=GROOVE,command=stream_server,text='Open Cam & Stream',font=('helvetica 15 bold'))
but3.place(x=5,y=250)

but4=Button(frame,padx=5,pady=5,width=39,bg='white',fg='black',relief=GROOVE,command=join_to_theater,text='Join to Theater',font=('helvetica 15 bold'))
but4.place(x=5,y=322)


but5=Button(frame,padx=5,pady=5,width=5,bg='white',fg='black',relief=GROOVE,text='EXIT',command=exitt,font=('helvetica 15 bold'))
but5.place(x=210,y=400)


root.mainloop()