import cv2
import numpy as np

cap = cv2.VideoCapture(0)
# setting height
cap.set(3, 640)
# setting width
cap.set(4, 480)
cap.set(10, 150)

myColor = [[73, 60, 54, 109, 185, 255], [158, 135, 127, 179, 229, 255]]

# BGR format
colorVal = [[16, 81, 20], [109, 46, 236]]

myPoints = []


def findColor(img, myColor):
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    newPoints = []
    cnt = 0
    for i in myColor:
        lower = np.array(i[0:3])
        upper = np.array(i[3:6])
        mask = cv2.inRange(imgHSV, lower, upper)
        x, y = getContours(mask)
        cv2.circle(imgResult, (x, y), 10, colorVal[cnt], cv2.FILLED)
        # cv2.imshow("img", mask)

        if x != 0 and y != 0:
            newPoints.append([x, y, cnt])
        cnt += 1
    return newPoints


def getContours(img):
    contours, hierarchy = cv2.findContours(
        img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    x, y, w, h = 0, 0, 0, 0
    for cnt in contours:
        area = cv2.contourArea(cnt)

        if area > 500:
            # cv2.drawContours(imgResult, cnt, -1, (255, 0, 0), 3)
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02*peri, True)
            # print(approx)
            x, y, w, h = cv2.boundingRect(approx)
    return x+w//2, y


def drawOnCanvas(points, colorVal):
    for point in points:
        cv2.circle(imgResult, (point[0], point[1]),
                   10, colorVal[point[2]], cv2.FILLED)


while True:
    # video = images frames, will store all frames and display with img
    # success - boolean var if video captured succefully or not
    success, img = cap.read()
    imgResult = img.copy()
    newPoints = findColor(img, myColor)

    if len(newPoints) != 0:
        for itr in newPoints:
            myPoints.append(itr)
    # print(myPoints)
    if len(myPoints) != 0:
        drawOnCanvas(myPoints, colorVal)

    cv2.imshow("Result", imgResult)
    # if q is pressed video will be stopped
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
