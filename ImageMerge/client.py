import numpy
from pygame import mixer
import time
import cv2
from tkinter import *
import tkinter.messagebox
from tkinter import filedialog as fd

import socket
import struct
import time
import pickle
import imutils


HOST=''
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


class popupWindow(object):
    def __init__(self,master):
        top=self.top=Toplevel(master)
        self.l=Label(top,text="Enter Server IP")
        self.l.pack()
        self.e=Entry(top)
        self.e.pack()
        self.b=Button(top,text='Ok',command=self.cleanup)
        self.b.pack()
    def cleanup(self):
        global HOST
        HOST=self.e.get()
        self.top.destroy()
        
def popup(master):
   w=popupWindow(master) 
   master.wait_window(w.top)



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
   global entry
   global HOST
   popup(root)
   cv2.namedWindow("Trackbars")
   cv2.resizeWindow("Trackbars",200,200)

   cv2.createTrackbar("L-H","Trackbars",0,179,nothing)
   cv2.createTrackbar("L-S","Trackbars",0,255,nothing)
   cv2.createTrackbar("L-V","Trackbars",0,255,nothing)
   cv2.createTrackbar("U-H","Trackbars",179,255,nothing)
   cv2.createTrackbar("U-S","Trackbars",255,255,nothing)
   cv2.createTrackbar("U-V","Trackbars",255,255,nothing)


   client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   cam=None
   
   try:
      
      client_socket.connect((HOST, 8485))
      ip=entry.get()
      entry.select_clear()
      cam = cv2.VideoCapture('http://'+ip+':4747/video')
      

      #encode to jpeg format
      #encode param image quality 0 to 100. default:95
      #if you want to shrink data size, choose low image quality.
      encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),90]


      while True:
         ret, frame = cam.read()

         frame = cv2.resize(frame, (600, 450))
         #image = cv2.resize(image, (600, 450))
         hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
         #hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

         L_H=cv2.getTrackbarPos("L-H","Trackbars")
         L_S=cv2.getTrackbarPos("L-S","Trackbars")
         L_V=cv2.getTrackbarPos("L-V","Trackbars")
         U_H=cv2.getTrackbarPos("U-H","Trackbars")
         U_S=cv2.getTrackbarPos("U-S","Trackbars")
         U_V=cv2.getTrackbarPos("U-V","Trackbars")

         u_green = numpy.array([U_H,U_S,U_V])
         l_green = numpy.array([L_H,L_S,L_V])

         mask = cv2.inRange(frame, l_green, u_green)

         res = cv2.bitwise_and(frame, frame, mask = mask)

         frame1 = frame - res

         cv2.imshow('My Video',cv2.resize(frame1, (600, 450)))


         frame = cv2.flip(frame,180)
         result, image = cv2.imencode('.jpg', frame, encode_param)
         data = pickle.dumps(image, 0)
         size = len(data)


         client_socket.sendall(struct.pack(">L", size) + data)
         
         if cv2.waitKey(1) & 0xFF == ord('q'):
            break

      client_socket.close()
      cam.release()
      cv2.destroyAllWindows()
   except:
     client_socket.close()
     if cam!=None:
      cam.release()
     cv2.destroyAllWindows()
     show_alert("Some thing goes wrong")
     alert()
   
def nothing (args):
    pass  

def stream_server():

   global entry
   global HOST
   global root
   popup(root)

   #image = cv2.imread("bg12.jpg")
    
   cv2.namedWindow("Trackbars")
   cv2.resizeWindow("Trackbars",200,200)

   cv2.createTrackbar("L-H","Trackbars",0,179,nothing)
   cv2.createTrackbar("L-S","Trackbars",0,255,nothing)
   cv2.createTrackbar("L-V","Trackbars",0,255,nothing)
   cv2.createTrackbar("U-H","Trackbars",179,255,nothing)
   cv2.createTrackbar("U-S","Trackbars",255,255,nothing)
   cv2.createTrackbar("U-V","Trackbars",255,255,nothing)


   client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   cam=None
   try:
      
      client_socket.connect((HOST, 8485))
      ip=entry.get()
      entry.select_clear()
      cam = cv2.VideoCapture(0)

      #cam = cv2.VideoCapture(0)
      bg = cv2.imread("bg.jpeg")
      bg = cv2.resize(bg, (600, 450))
      

      #encode to jpeg format
      #encode param image quality 0 to 100. default:95
      #if you want to shrink data size, choose low image quality.
      encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),90]


      while True:
         ret, frame = cam.read()

         frame = cv2.resize(frame, (600, 450))
         #image = cv2.resize(image, (600, 450))
         hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
         #hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

         L_H=cv2.getTrackbarPos("L-H","Trackbars")
         L_S=cv2.getTrackbarPos("L-S","Trackbars")
         L_V=cv2.getTrackbarPos("L-V","Trackbars")
         U_H=cv2.getTrackbarPos("U-H","Trackbars")
         U_S=cv2.getTrackbarPos("U-S","Trackbars")
         U_V=cv2.getTrackbarPos("U-V","Trackbars")

         u_green = numpy.array([U_H,U_S,U_V])
         l_green = numpy.array([L_H,L_S,L_V])

         mask = cv2.inRange(frame, l_green, u_green)

         res = cv2.bitwise_and(frame, frame, mask = mask)

         frame1 = frame - res

         frame_test = numpy.where(frame1 == 0, bg, frame1)


         cv2.imshow('My Video',cv2.resize(frame1, (600, 450)))


         #frame = imutils.resize(frame1, width=1250)
         frame = cv2.flip(frame1,180)
         result, image = cv2.imencode('.jpg', frame, encode_param)
         data = pickle.dumps(image, 0)
         size = len(data)


         client_socket.sendall(struct.pack(">L", size) + data)
         
         if cv2.waitKey(1) & 0xFF == ord('q'):
            break

      client_socket.close()
      cam.release()
      cv2.destroyAllWindows()
   except:
     client_socket.close()
     if cam!=None:
      cam.release()
     cv2.destroyAllWindows()
     show_alert("Some thing goes wrong")
     alert()
   
   
   
def join_to_theater():
   global HOST
   popup(root)
   conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   try:
      conn.connect((HOST, 8080))

      data = b""
      payload_size = struct.calcsize(">L")
      print("payload_size: {}".format(payload_size))
      while True:
         while len(data) < payload_size:
            chunk=conn.recv(4096)
            if chunk == b'':
               raise RuntimeError("socket connection broken")
            data += chunk
         # receive image row data form client socket
         packed_msg_size = data[:payload_size]
         data = data[payload_size:]
         msg_size = struct.unpack(">L", packed_msg_size)[0]
         while len(data) < msg_size:
            chunk=conn.recv(4096)
            if chunk == b'':
               raise RuntimeError("socket connection broken")
            data += chunk
         frame_data = data[:msg_size]
         data = data[msg_size:]
         # unpack image using pickle 
         frame=pickle.loads(frame_data, fix_imports=True, encoding="bytes")
         frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)

         cv2.imshow('Theater',frame)
         if cv2.waitKey(1) & 0xFF == ord('q'):
               break
         # cv2.waitKey(1)  
      conn.close()   
      cv2.destroyAllWindows()
   except:
     conn.close()   
     cv2.destroyAllWindows()
     show_alert("Some thing goes wrong")
     alert()

   

def show_alert(msg):
   tkinter.messagebox.showinfo("Alert",msg)
   
def alert():
   mixer.init()
   alert=mixer.Sound('beep-07.wav')
   alert.play()
   time.sleep(0.1)
   alert.play()   
   
def select_file():
    global HOST
    popup(root)
    encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),90]
    filetypes = (
        ('jpeg files', '*.jpeg'),
        ('jpg files', '*.jpg'),
    )

    file = fd.askopenfilename(
        title='Open a file',
        initialdir='/',
        filetypes=filetypes)
    if len(file)!=0:
      try:
         client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
         client_socket.connect((HOST, 8486))
         bg=cv2.imread(file)
         frame = cv2.flip(bg,180)
         result, image = cv2.imencode('.jpg', frame, encode_param)
         data = pickle.dumps(image, 0)
         size = len(data)
         client_socket.sendall(struct.pack(">L", size) + data)
      except:
         show_alert("Background upload failed")
         alert()
      
    
       
    



entry= Entry(frame, width= 30,bg='white',bd =5,fg='green')
entry.focus_set()
entry.place(x=100,y=140)
   

but1=Button(frame,padx=5,pady=5,width=39,bg='white',fg='black',relief=GROOVE,command=open_cam,text='Open Droid web Cam & Stream',font=('helvetica 15 bold'))
but1.place(x=5,y=176)

but3=Button(frame,padx=5,pady=5,width=39,bg='white',fg='black',relief=GROOVE,command=stream_server,text='Open Cam & Stream',font=('helvetica 15 bold'))
but3.place(x=5,y=250)


but4=Button(frame,padx=5,pady=5,width=39,bg='white',fg='black',relief=GROOVE,command=join_to_theater,text='Join to Theater',font=('helvetica 15 bold'))
but4.place(x=5,y=322)

open_button = Button(frame,padx=5,pady=5,width=39,bg='white',fg='black',relief=GROOVE,font=('helvetica 15 bold'),text='Upload Background',command=select_file)
open_button.place(x=5,y=400)

but5=Button(frame,padx=5,pady=5,width=5,bg='white',fg='black',relief=GROOVE,text='EXIT',command=exitt,font=('helvetica 15 bold'))
but5.place(x=210,y=480)


root.mainloop()