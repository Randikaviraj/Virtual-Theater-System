import cv2
import numpy as np
print(cv2.__version__)
import numpy as np
 
video1 = cv2.VideoCapture("green7.mp4")
video2 = cv2.VideoCapture("green2.mp4")
image = cv2.imread("bg12.jpg")



def nothing ():
    pass

cv2.namedWindow("Trackbars")
cv2.resizeWindow("Trackbars",200,200)

cv2.createTrackbar("L-H","Trackbars",0,179,nothing)
cv2.createTrackbar("L-S","Trackbars",0,255,nothing)
cv2.createTrackbar("L-V","Trackbars",0,255,nothing)
cv2.createTrackbar("U-H","Trackbars",179,255,nothing)
cv2.createTrackbar("U-S","Trackbars",255,255,nothing)
cv2.createTrackbar("U-V","Trackbars",255,255,nothing)


cv2.namedWindow("Trackbars_2")
cv2.resizeWindow("Trackbars_2",200,200)

cv2.createTrackbar("L-H","Trackbars_2",0,179,nothing)
cv2.createTrackbar("L-S","Trackbars_2",0,255,nothing)
cv2.createTrackbar("L-V","Trackbars_2",0,255,nothing)
cv2.createTrackbar("U-H","Trackbars_2",179,255,nothing)
cv2.createTrackbar("U-S","Trackbars_2",255,255,nothing)
cv2.createTrackbar("U-V","Trackbars_2",255,255,nothing)

while True:
 
    ret1, frame1  = video1.read()
    ret2, frame2=video2.read()
 
    frame1 = cv2.resize(frame1, (600, 450))
    frame2 = cv2.resize(frame2, (600, 450))
    #print(frame[20][20])
    image = cv2.resize(image, (600, 450))
    #cv2.imshow("bg",image)
    #hsv=cv2.cvtColor(frame,cv2.COlOR_BGR2HSV)
    hsv1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2HSV)
    hsv2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2HSV)
    #print(cv2.cvtColor(frame, cv2.COLOR_BGR2HSV))
    L_H=cv2.getTrackbarPos("L-H","Trackbars")
    L_S=cv2.getTrackbarPos("L-S","Trackbars")
    L_V=cv2.getTrackbarPos("L-V","Trackbars")
    U_H=cv2.getTrackbarPos("U-H","Trackbars")
    U_S=cv2.getTrackbarPos("U-S","Trackbars")
    U_V=cv2.getTrackbarPos("U-V","Trackbars")

    u_green = np.array([U_H,U_S,U_V])
    l_green = np.array([L_H,L_S,L_V])


    L_H2=cv2.getTrackbarPos("L-H","Trackbars_2")
    L_S2=cv2.getTrackbarPos("L-S","Trackbars_2")
    L_V2=cv2.getTrackbarPos("L-V","Trackbars_2")
    U_H2=cv2.getTrackbarPos("U-H","Trackbars_2")
    U_S2=cv2.getTrackbarPos("U-S","Trackbars_2")
    U_V2=cv2.getTrackbarPos("U-V","Trackbars_2")

    u_green = np.array([U_H,U_S,U_V])
    l_green = np.array([L_H,L_S,L_V])

    u_green2 = np.array([U_H2,U_S2,U_V2])
    l_green2 = np.array([L_H2,L_S2,L_V2])

    #u_green2 = np.array([66, 184, 125])
    #l_green2 = np.array([0, 93, 19])

    mask1 = cv2.inRange(frame1, l_green, u_green)
    mask2 = cv2.inRange(frame2, l_green2, u_green2)
    #print(mask)
    #u_green = np.array([104, 153, 70])
    #l_green = np.array([30, 30, 0])
 
    #mask = cv2.inRange(frame, l_green, u_green)
    cv2.imshow("mask1", mask1)
    cv2.imshow("mask2", mask2)
    res1 = cv2.bitwise_and(frame1, frame1, mask = mask1)
    
    res2 = cv2.bitwise_and(frame2, frame2, mask = mask2)
    #cv2.imshow("res2", res2)
    
    
    f1 = frame1 - res1 
    f2 = frame2 - res2
    #cv2.imshow("fpre", f)
    ff = np.where(f1 == 0, f2, f1)
    fff = np.where(ff == 0, image, ff)
    kernel = np.ones((2,2),np.float32)/4
    dst = cv2.filter2D(fff,-1,kernel)

    #kernel = np.array([[0, -1, 0],
    #               [-1, 5,-1],
    #               [0, -1, 0]])
    #image_sharp = cv2.filter2D(src=f, ddepth=-1, kernel=kernel)
    #cv2.imshow("video", frame)
    cv2.imshow("fff", fff)
    #cv2.imshow("dst", dst)

 
    if cv2.waitKey(25) == 27:
        break
 
video.release()
cv2.destroyAllWindows()