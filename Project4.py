import cv2
import numpy as np

cap = cv2.VideoCapture(0)
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# fourcc = cv2.VideoWriter_fourcc('X', 'V', 'I', 'D')

# out = cv2.VideoWriter("output.avi", fourcc, 5.0, (1280, 720))

ret, frame1 = cap.read()
ret, frame2 = cap.read()
# print(frame1.shape)


while cap.isOpened():
    diff = cv2.absdiff(frame1, frame2)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blur, 18, 255, cv2.THRESH_BINARY) # thresh of 5 reconize breathing. 2 will reconize pulse!!

    # Breath recognition options
    # 1. remove all big motions - dilate only breathing (only if tempo is correct)
    # 2. focus on torso - dilate only torso

    dilated = cv2.dilate(thresh, None, iterations=3)

    # cv2.imshow("feed", dilated)

    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        (x, y, w, h) = cv2.boundingRect(contour)

        if cv2.contourArea(contour) < 900:
            continue
        cv2.rectangle(frame1, (x, y), (x+w, y+h), (0, 150, 255), 2)
        # cv2.putText(frame1, "Status: {}".format('Movement'), (10, 20), cv2.FONT_HERSHEY_SIMPLEX,1, (0, 0, 255), 3)
    # cv2.drawContours(frame1, contours, -1, (0, 255, 0), 2)

    image = cv2.resize(frame1, (1280, 720))
    # out.write(image)

    cv2.imshow("feed", frame1)
    # cv2.imshow("feed", diff)
    # cv2.imshow("feed", dilated)


    frame1 = frame2
    ret, frame2 = cap.read()

    if cv2.waitKey(40) == 27:
        break

cv2.destroyAllWindows()
cap.release()

# out.release()

