import cv2
from djitellopy import Tello
import mediapipe as mp

mp_hands = mp.solutions.hands
mp_pose = mp.solutions.pose
mp_face = mp.solutions.face_detection
tello = Tello()
tello.connect()

tello.takeoff()
tello.streamon()

for _ in range(3):
    tello.rotate_clockwise(120)
    break


with mp_hands.Hands(min_detection_confidence=0.4, min_tracking_confidence=0.7) as hands, \
        mp_pose.Pose(min_detection_confidence=0.7, min_tracking_confidence=0.7) as pose, \
        mp_face.FaceDetection(min_detection_confidence=0.9) as face_detection:
    while True:
        frame = tello.get_frame_read().frame
             

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        hands_results = hands.process(rgb_frame)
        pose_results = pose.process(rgb_frame)
        face_results = face_detection.process(rgb_frame)

        if face_results.detections and not pose_results.pose_landmarks:
            tello.land()



        if pose_results.pose_landmarks:
            mp.solutions.drawing_utils.draw_landmarks(frame, pose_results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

            left_hand_midpoint = (
                int((pose_results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_WRIST].x +
                     pose_results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_PINKY].x) * frame.shape[1] / 2),
                int((pose_results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_WRIST].y +
                     pose_results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_PINKY].y) * frame.shape[0] / 2)
            )
            right_hand_midpoint = (
                int((pose_results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_WRIST].x +
                     pose_results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_PINKY].x) * frame.shape[1] / 2),
                int((pose_results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_WRIST].y +
                     pose_results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_PINKY].y) * frame.shape[0] / 2)
            )

            hands_distance = ((left_hand_midpoint[0] - right_hand_midpoint[0]) ** 2 +
                              (left_hand_midpoint[1] - right_hand_midpoint[1]) ** 2) ** 0.5

            if hands_distance > 50:
                tello.move_forward(70)
            else:
                tello.flip_back()
        battery_percentage = tello.query_battery()
        cv2.putText(frame, f'Battery: {battery_percentage}%', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)

        cv2.imshow('Tello Pose and Hand Detection', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


tello.streamoff()
tello.land()
tello.disconnect()

cv2.destroyAllWindows()
