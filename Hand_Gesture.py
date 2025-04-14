
import cv2
import mediapipe as mp
import time
import pydirectinput

def detect_fingers(hand_landmarks):
    """Detect which fingers are up based on Mediapipe landmarks."""
    fingers = [0, 0, 0, 0, 0]  # Thumb, Index, Middle, Ring, Pinky
    
    if hand_landmarks[4].x < hand_landmarks[3].x:  # Thumb Open
        fingers[0] = 1
    if hand_landmarks[8].y < hand_landmarks[6].y:  # Index Finger
        fingers[1] = 1
    if hand_landmarks[12].y < hand_landmarks[10].y:  # Middle Finger
        fingers[2] = 1
    if hand_landmarks[16].y < hand_landmarks[14].y:  # Ring Finger
        fingers[3] = 1
    if hand_landmarks[20].y < hand_landmarks[18].y:  # Pinky Finger
        fingers[4] = 1
    
    return fingers

def main():
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
    mp_draw = mp.solutions.drawing_utils
    cap = cv2.VideoCapture(0)
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb_frame)
        
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                fingers = detect_fingers(hand_landmarks.landmark)
                
                if fingers == [0, 1, 0, 0, 0]:
                    print("Left")
                    pydirectinput.press("left")
                elif fingers == [0, 0, 0, 0, 1]:
                    print("Right")
                    pydirectinput.press("right")
                elif fingers == [0, 1, 1, 0, 0]:
                    print("Up")
                    pydirectinput.press("up")
                elif fingers == [0, 0, 0, 0, 0]:
                    print("Down")
                    pydirectinput.press("down")
                elif fingers == [0, 1, 0, 0, 1]:
                    print("Ability (Hoverboard)")
                    pydirectinput.press("space")
        
        cv2.imshow("Hand Gesture Game Controller", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()
    
if __name__ == "__main__":
    main()
