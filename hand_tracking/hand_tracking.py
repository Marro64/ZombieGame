import cv2
from cvzone.HandTrackingModule import HandDetector

class HandTracking:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.detector = HandDetector(detectionCon=0.8, maxHands=2)
        self.lmList1 = None
        self.centerPoint1 = None
        self.fingers1 = None

    def update(self):
        success, img = self.cap.read()
        # print(type(img))
        hands, img = self.detector.findHands(img)  # With Draw
        # hands = detector.findHands(img, draw=False)  # No Draw

        if hands:
            # Hand 1
            hand1 = hands[0]
            self.lmList1 = hand1["lmList"]  # List of 21 Landmarks points
            bbox1 = hand1["bbox"]  # Bounding Box info x,y,w,h
            self.centerPoint1 = hand1["center"]  # center of the hand cx,cy
            handType1 = hand1["type"]  # Hand Type Left or Right

            # print(len(lmList1),lmList1)
            # print(bbox1)
            # print(centerPoint1)
            self.fingers1 = self.detector.fingersUp(hand1)
            #length, info, img = detector.findDistance(lmList1[8], lmList1[12], img) # with draw
            #length, info = detector.findDistance(lmList1[8], lmList1[12])  # no draw


            if len(hands) == 2:
                hand2 = hands[1]
                lmList2 = hand2["lmList"]  # List of 21 Landmarks points
                bbox2 = hand2["bbox"]  # Bounding Box info x,y,w,h
                centerPoint2 = hand2["center"]  # center of the hand cx,cy
                handType2 = hand2["type"]  # Hand Type Left or Right

                fingers2 = self.detector.fingersUp(hand2)
                # # print(fingers1, fingers2)
                # #length, info, img = detector.findDistance(lmList1[8], lmList2[8], img) # with draw
                # length, info, img = self.detector.findDistance(centerPoint1, centerPoint2, img)  # with draw

        cv2.imshow("Image", img)
        cv2.waitKey(1)

    def get_point(self, point = -1):
        if self.lmList1 is not None:
            if 0 <= point < 21:
                return self.lmList1[point]
            else:
                return self.lmList1

    def get_center(self):
        return self.centerPoint1

    def get_finger_up(self, finger=1):
        if self.fingers1 is not None:
            return self.fingers1[finger] == 1
        else:
            return False


if __name__ == "__main__":
    HandTracker = HandTracking()
    while True:
        HandTracker.update()

