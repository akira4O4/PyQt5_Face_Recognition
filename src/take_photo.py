import cv2


class Camera:
    global cap
    cap = cv2.VideoCapture(0)
    num = 1  # 照片计数器

    def __init__(self):
        pass

    def openCamera(self):
        cap.open()
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)
        frame = cv2.resize(frame, (640, 480))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        lable = cv2.putText(frame, '-->Camera OK', (10, 30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 255, 0),
                            thickness=1, lineType=1)
        return frame

    def takePhoto(self):
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)
        frame = cv2.resize(self.frame, (640, 480))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        lable = cv2.putText(frame, '-->Press the space to take a photo', (10, 30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1,
                            (0, 255, 0),
                            thickness=1, lineType=1)


if __name__ == "__main__":
    # cap=Camera()
    # cap.openCamera()
    selectFName = 'ff'
    fPaht = '../faces/' + selectFName
