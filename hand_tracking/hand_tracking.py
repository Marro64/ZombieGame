import cv2
from cvzone.HandTrackingModule import HandDetector

# Hand tracking module derived from https://www.computervision.zone/courses/multiple-hand-gesture-control/

class HandTracking:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.detector = HandDetector(detectionCon=0.8, maxHands=2)
        self.lmList1 = None
        self.centerPoint1 = None
        self.fingers1 = None

    def update(self):
        success, img = self.cap.read()
        hands, img = self.detector.findHands(img)  # With Draw

        if hands:
            # Hand 1
            hand1 = hands[0]
            self.lmList1 = hand1["lmList"]  # List of 21 Landmarks points
            self.centerPoint1 = hand1["center"]  # center of the hand cx,cy
            self.fingers1 = self.detector.fingersUp(hand1)


            if len(hands) == 2:
                hand2 = hands[1]

                fingers2 = self.detector.fingersUp(hand2)

        # cv2.imshow("Image", img)
        # cv2.waitKey(1)

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

