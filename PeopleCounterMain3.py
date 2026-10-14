import argparse
import datetime
import imutils
import math
import cv2
from time import time, ctime
import numpy as np
from openpyxl import Workbook
from openpyxl import load_workbook
import openpyxl
import datetime
import xlsxwriter

width = 800

IN_CHECK = 250
IN_CONSEC_FRAMES = 150
TOTAL_IN = 0
COUNTER_IN = 0

OUT_CHECK = 150
OUT_CONSEC_FRAMES = 150
TOTAL_OUT = 0
COUNTER_OUT = 0
countrow = 0
total_list = []
if __name__ == "__main__":
    camera = cv2.VideoCapture("TestVideo.avi")

    firstFrame = None
    
    # loop over the frames of the video
    while True:
        # grab the current frame and initialize the occupied/unoccupied
        # text
        (grabbed, frame) = camera.read()
        text = "Unoccupied"

        # if the frame could not be grabbed, then we have reached the end
        # of the video
        if not grabbed:
            break

        # resize the frame, convert it to grayscale, and blur it
        frame = imutils.resize(frame, width=width)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        # if the first frame is None, initialize it
        if firstFrame is None:
            firstFrame = gray
            continue

        # compute the absolute difference between the current frame and
        # first frame
        frameDelta = cv2.absdiff(firstFrame, gray)
        thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
        # dilate the thresholded image to fill in holes, then find contours
        # on thresholded image
        thresh = cv2.dilate(thresh, None, iterations=2)
        cv2.imshow("thresh", thresh)
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
        # loop over the contours
        for c in cnts:
            #print(c)
            # if the contour is too small, ignore it
            if cv2.contourArea(c) < 3000:
                continue
            # compute the bounding box for the contour, draw it on the frame,
            # and update the text
            (x, y, w, h) = cv2.boundingRect(c)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            #cv2.line(frame, (width // 2, 0), (width, 450), (250, 0, 1), 2)  # blue line
            #cv2.line(frame, (width // 2 - 50, 0), (width - 50, 450), (0, 0, 255), 2)  # red line
            cv2.line(frame,(0,400),(800,400),(255,0,0),1)
            cv2.line(frame,(0,300),(800,300),(0,0,255),1)

            rectagleCenterPont = ((x + x + w) // 2, (y + y + h) // 2)
            cv2.circle(frame, rectagleCenterPont, 1, (0, 0, 255), 5)
            ear = (x + x + w) // 2
            #print(ear)
            if (ear > IN_CHECK):
                COUNTER_IN += 1
#                 print(COUNTER_IN)
            else:
                if COUNTER_IN >= IN_CONSEC_FRAMES:
                    TOTAL_IN += 1
                # reset the eye frame counter
                    COUNTER_IN = 0
                    
            #print(ear)
            if (ear < OUT_CHECK):
                COUNTER_OUT += 1
#                 print(COUNTER_OUT)
            else:
                if COUNTER_OUT >= OUT_CONSEC_FRAMES:
                    TOTAL_OUT += 1
                # reset the eye frame counter
                    COUNTER_OUT = 0
                    
            if TOTAL_OUT > TOTAL_IN:
                Amount = 0
            else:
                Amount = TOTAL_IN - TOTAL_OUT
                    
            cv2.putText(frame, "Amout: {}".format(str(Amount)), (10, 90),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            # draw the text and timestamp on the frame

            # show the frame and record if the user presses a key
            # cv2.imshow("Thresh", thresh)
            # cv2.imshow("Frame Delta", frameDelta)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        #cv2.line(frame, (width // 2, 0), (width, 450), (250, 0, 1), 2)  # blue line
        #cv2.line(frame, (width // 2 - 50, 0), (width - 50, 450), (0, 0, 255), 2)  # red line

        #cv2.line(frame, (0,0),(1000,1000), (250, 0, 1), 2)  # blue line
        #cv2.line(frame, (0,50),(1000,1000), (0, 0, 255), 2)  # red line

        
        cv2.putText(frame, "In: {}".format(str(TOTAL_IN)), (10, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        cv2.putText(frame, "Out: {}".format(str(TOTAL_OUT)), (10, 70),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
                    (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
        cv2.imshow("Security Feed", frame)

        xTime = datetime.datetime.now()
        tt=str(xTime.day)+str(xTime.month)+':'+str(xTime.year)+':'+str(xTime.hour)+':'+str(xTime.minute)+':'+str(xTime.second)+':'+'Amount:'+str(Amount)
        total_list.append(tt)
        workbook  = xlsxwriter.Workbook('filenameffff11.xlsx')
        worksheet = workbook.add_worksheet()
        expenses = (total_list)
        # Start from the first cell. Rows and columns are zero indexed.
        row = 0
        # Iterate over the data and write it out row by row.
        for item in (expenses):
            print('item',item)
            worksheet.write(row, 0, item)
            row += 1
        
        workbook.close() 

    # cleanup the camera and close any open windows
    camera.release()
    cv2.destroyAllWindows()
