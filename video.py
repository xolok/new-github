import cv2
import numpy as np
import argparse
from visualizecv2 import model, display_instances, class_names

# ap = argparse.ArgumentParser()
# ap.add_argument("-v", "--video", required=True, help = "path to input video file")
# args = vars(ap.parse_args())

# capture = cv2.VideoCapture(args["video"])
capture = cv2.VideoCapture('how.mp4')

size = (
    int(capture.get(cv2.CAP_PROP_FRAME_WIDTH)),
    int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
)
fps = capture.get(cv2.CAP_PROP_FPS)      # OpenCV2 version 2 used "CV_CAP_PROP_FPS"
frame_count = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
duration = frame_count/fps

print('fps = ' + str(fps))
print('number of frames = ' + str(frame_count))
print('duration (S) = ' + str(duration))
# length = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
# length1 = capture.get(cv2.CAP_PROP_FRAME_COUNT)
# time  = capture.get(cv2.CAP_PROP_POS_MSEC)
# print(time)
# spf = time/length1
codec = cv2.VideoWriter_fourcc(*'DIVX')
output = cv2.VideoWriter('video_new_22.avi', codec, 60.0, size)

# index will give the no. of frames where the event is detected
# x1 stores the list of the mask coordinates of detected frames
# framex is a list of all the frames where an event is detected
# timex is the list of the time of all the frames where an event is detected
# num is the number of frames of the original video to be detected 
# diff is the difference between two frames to be seen simultaneously 
# alpha is the opaqueness of the addition of two framws
# xcoor,ycoor is a list of list of bbox of all the detected frames
# labelx is the time index of all the the detected frames

index = 0
x1 = []
framex = []
timex = []
num = 1206
diff = 220
alpha = .8
xcoor = []
ycoor = [] 
labelx = []
# while(capture.isOpened()):
# count = 0
#The video detection part
while(index<num):
    ret, frame = capture.read()
    
    if ret:
        # add mask to frame
        framex.append(frame)
        results = model.detect([frame], verbose=0)
        r = results[0]
        print(index)
        timex.append(index/fps)
        print(index/fps)
        time1 = index/fps
        frame,point,xcoor1,ycoor1,label1 = display_instances(
            frame, r['rois'], r['masks'], r['class_ids'], class_names , r['scores'],time1
        )

        xcoor.append(xcoor1)
        ycoor.append(ycoor1)
        labelx.append(label1)
        # print(np.shape(frame))
        # print(np.shape(r['masks']))
        x = np.where(r['masks']==True)
        
        # output.write(frame)
        # cv2.imshow('frame', frame)
        x1.append(x[0:2])
        # print(np.shape(x1[index]))
        index = index+1
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     break
    else:
        break

#This part uses the detected info from the above code make save it in an output video;
for i in range(diff,num):
    xco = xcoor[i]
    yco = ycoor[i]
    lab = labelx[i]
    xcop = xcoor[i-diff]
    ycop = ycoor[i-diff]
    labp = labelx[i-diff]
    x2 = x1[i-diff][0]
    x3 = x1[i-diff][1]
    frame1 = framex[i]
    for j in range(len(x2)):
        frame1[x2[j]][x3[j]] = alpha*framex[i-diff][x2[j]][x3[j]] + alpha*framex[i][x2[j]][x3[j]] 
    for j in range(len(xcop)):
        frame1 = cv2.putText(frame1, labp[j],
                    (xcop[j],ycop[j]), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    for j in range(len(xco)):
        frame1 = cv2.putText(frame1, lab[j],
                    (xco[j],yco[j]), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    
    # file_name = "./output/" + str(count) + ".JPG"
    # cv2.imwrite(file_name,frame1)
    # count += 1
    #cv2.imshow('frame', frame1)

    output.write(frame1)
    if cv2.waitKey(1) & 0xFF == ord('q'):
            break

capture.release()
# output.release()
cv2.destroyAllWindows()