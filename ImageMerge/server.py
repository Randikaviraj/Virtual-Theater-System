import socket
import sys
import cv2
import threading
import pickle
import struct ## new
import imutils
import numpy as np

HOST='127.0.0.1'
PORT=8485
lock=threading.Lock()
clint_lock=threading.Lock()


def algorithm(frames):
    if len(frames)==1:
        return frames[0]
    if len(frames)==2:
        return frames[1]
    if len(frames)==3:
        ff = np.where(frames[1] == 0, frames[2], frames[1])
        fff = np.where(ff == 0, frames[0], ff)
        return fff
    else :
	    pass
        
    

def client_request_handling(client_request_socket_list):
    global HOST
    port =8080
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.bind((HOST,port))
    s.listen(10)
    print('Clint Socket now listening')
    while True:
        conn,addr=s.accept()
        clint_lock.acquire()
        client_request_socket_list.append(conn)
        clint_lock.release()

    

def theater_room(socket_list,client_request_socket_list):
    encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),90]
    bg = cv2.imread("bg.jpeg", cv2.IMREAD_COLOR)
    payload_size = struct.calcsize(">L")
    print("payload_size: {}".format(payload_size))
    while True:
        frames=[]
        frames.append(bg)
        lock.acquire()
        for i,(conn,data)  in enumerate(socket_list): 
            try:
                
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
                socket_list[i]=(conn,data)
                # unpack image using pickle 
                frame=pickle.loads(frame_data, fix_imports=True, encoding="bytes")
                frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)

                # cv2.imshow('server',frame)
                cv2.waitKey(1)
                frames.append(frame)
                
            except socket.error as msg:
                print("Socket exception occurred")
                socket_list.remove((conn,data))
            except:
                socket_list.remove((conn,data))
                print('An exception occurred')    
              
        lock.release()
        merged_frame=algorithm(frames=frames)
        merged_frame = imutils.resize(merged_frame, width=1250)
        merged_frame = cv2.flip(merged_frame,180)
        result, image = cv2.imencode('.jpg', merged_frame, encode_param)
        data = pickle.dumps(image, 0)
        size = len(data)
        
        clint_lock.acquire()
        for conn in client_request_socket_list:
            try:
              conn.sendall(struct.pack(">L", size) + data)
            except socket.error as msg:
                client_request_socket_list.remove(conn)
            except:
              print('An exception occurred')
            
        clint_lock.release()
            
            
        
        
def streamer_request_handling(socket_list):
    global HOST
    port=8485
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
    s.bind((HOST,port))

    s.listen(10)
    print('Stream Socket now listening')
    while True:
        conn,addr=s.accept()
        lock.acquire()
        socket_list.append((conn,b"" ))
        lock.release()


socket_list=[]
client_request_socket_list=[]

threading.Thread(target=streamer_request_handling,args=(socket_list,)).start()
threading.Thread(target=theater_room,args=(socket_list,client_request_socket_list,)).start()
threading.Thread(target=client_request_handling,args=(client_request_socket_list,)).start()







