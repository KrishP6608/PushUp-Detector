import cv2
import mediapipe as mp
import math

mp_drawing = mp.solutions.drawing_utils
drawSpecific = mp.solutions.pose
mp_pose = mp.solutions.pose

pushUp_counter = 0
pushUp_started = 0

cam = cv2.VideoCapture(0)

with mp_pose.Pose(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as pose:
    while True:
        shown, frame = cam.read()
        if not shown:
            print("Camera is not working")
            continue
        frame.flags.writeable = False
        results = pose.process(frame)
        frame_height, frame_width, _ = frame.shape

        leftShoulder = (int(results.pose_landmarks.landmark[11].x * frame_width),
                        int(results.pose_landmarks.landmark[11].y * frame_height))
        rightShoulder = (int(results.pose_landmarks.landmark[12].x * frame_width),
                         int(results.pose_landmarks.landmark[12].y * frame_height))
        leftElbow = (int(results.pose_landmarks.landmark[13].x * frame_width),
                        int(results.pose_landmarks.landmark[13].y * frame_height))
        rightElbow = (int(results.pose_landmarks.landmark[14].x * frame_width),
                            int(results.pose_landmarks.landmark[14].y * frame_height))
        leftWrist = (int(results.pose_landmarks.landmark[15].x * frame_width),
                        int(results.pose_landmarks.landmark[15].y * frame_height))
        rightWrist = (int(results.pose_landmarks.landmark[16].x * frame_width),
                            int(results.pose_landmarks.landmark[16].y * frame_height))

        cv2.circle(frame, leftShoulder, 5, (255, 0, 0), 15)
        cv2.circle(frame, rightShoulder, 5, (255, 0, 0), 15)
        cv2.circle(frame, leftElbow, 5, (255, 0, 0), 15)
        cv2.circle(frame, rightElbow, 5, (255, 0, 0), 15)
        cv2.circle(frame, leftWrist, 5, (255, 0, 0), 15)
        cv2.circle(frame, rightWrist, 5, (255, 0, 0), 15)
        cv2.line(frame, leftShoulder, leftElbow, (255, 0, 0), 5)
        cv2.line(frame, rightShoulder, rightElbow, (255, 0, 0), 5)
        cv2.line(frame, leftElbow, leftWrist, (255, 0, 0), 5)
        cv2.line(frame, rightElbow, rightWrist, (255, 0, 0), 5)

        angle = abs(math.degrees(math.atan2(rightShoulder[1] - rightElbow[1], rightShoulder[0] - rightElbow[0])
                             - math.atan2(rightWrist[1] - rightElbow[1], rightWrist[0] - rightElbow[0])))
        angle2 = abs(math.degrees(math.atan2(leftShoulder[1] - leftElbow[1], leftShoulder[0] - leftElbow[0])
                              - math.atan2(leftWrist[1] - leftElbow[1], leftWrist[0] - leftElbow[0])))

        if pushUp_started == 0:
            if angle <= 60 and angle2 <= 60:
                pushUp_started = 1
                pushUp_counter += 1
        elif pushUp_started == 1:
            if angle >= 140 and angle2 >= 140:
                pushUp_started = 0

        pushUps_Done = "Pushups Done: " + str(pushUp_counter)
        print(pushUps_Done)
        cv2.putText(frame, pushUps_Done, (50, 100), 1, 2, (0, 0, 0), 2)

        cv2.imshow("frame", frame)
        key = cv2.waitKey(1)
        if key == 27:
            break

cam.release()
cv2.destroyAllWindows()
