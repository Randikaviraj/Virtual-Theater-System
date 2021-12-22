import socket
import sys
import cv2
import threading
import pickle
import struct ## new
import imutils

HOST='127.0.0.1'
PORT=8485
lock=threading.Lock()
clint_lock=threading.Lock()


def algorithm(frames):
    if len(frames)==1:
        return frames[0]
    else:
        return frames[1]
        
    

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
    data = b""
    payload_size = struct.calcsize(">L")
    print("payload_size: {}".format(payload_size))
    while True:
        frames=[]
        bg = cv2.imread("bg.jpeg", cv2.IMREAD_COLOR)
        frames.append(bg)
        lock.acquire()
        for conn in socket_list:
            try:
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

                frames.append(frame)
                # cv2.imshow('server',frame)
                cv2.waitKey(1)
            except socket.error as msg:
                socket_list.remove(conn)
            except:
              print('An exception occurred')    
        lock.release()
        print(len(frames))
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
    print('Socket created')
    
    s.bind((HOST,port))
    print('Socket bind complete')
    s.listen(10)
    print('Stream Socket now listening')
    while True:
        conn,addr=s.accept()
        lock.acquire()
        socket_list.append(conn)
        lock.release()


socket_list=[]
client_request_socket_list=[]

threading.Thread(target=theater_room,args=(socket_list,client_request_socket_list,)).start()
threading.Thread(target=client_request_handling,args=(client_request_socket_list,)).start()
threading.Thread(target=streamer_request_handling,args=(socket_list,)).start()






