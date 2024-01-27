import cv2
import mediapipe as mp
import pyautogui
import numpy as np
from keras.models import model_from_json

cam = cv2.VideoCapture(0)

if not cam.isOpened():
    print("Error: Could not open camera.")
else:
    cam = cv2.VideoCapture(0)
    face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)
    screen_w, screen_h = pyautogui.size()

    # Load emotion detection model
    json_file = open("facialemotionmodel.json", "r")
    model_json = json_file.read()
    json_file.close()
    emotion_model = model_from_json(model_json)
    emotion_model.load_weights("facialemotionmodel.h5")

    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    def extract_features(image):
        feature = np.array(image)
        feature = feature.reshape(1, 48, 48, 1)
        return feature / 255.0

    try:
        while True:
            labels = {0: 'angry', 1: 'disgust', 2: 'fear', 3: 'happy', 4: 'neutral', 5: 'sad', 6: 'surprise'}

            _, frame = cam.read()
            frame = cv2.flip(frame, 1)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            output = face_mesh.process(rgb_frame)
            landmark_points = output.multi_face_landmarks
            frame_h, frame_w, _ = frame.shape
            if landmark_points:
                landmarks = landmark_points[0].landmark
                for id, landmark in enumerate(landmarks[474:478]):
                    x = int(landmark.x * frame_w)
                    y = int(landmark.y * frame_h)
                    cv2.circle(frame, (x, y), 3, (0, 255, 0))
                    if id == 1:
                        screen_x = screen_w / frame_w * x
                        screen_y = screen_h / frame_h * y
                        pyautogui.moveTo(screen_x, screen_y)
                left = [landmarks[145], landmarks[159]]
                for landmark in left:
                    x = int(landmark.x * frame_w)
                    y = int(landmark.y * frame_h)
                    cv2.circle(frame, (x, y), 3, (0, 255, 255))
                if (left[0].y - left[1].y) < 0.009:
                    pyautogui.click()
                    pyautogui.sleep(1)

                # Emotion detection
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(frame, 1.3, 5)
                try:
                    for (p, q, r, s) in faces:
                        image = gray[q:q + s, p:p + r]
                        cv2.rectangle(frame, (p, q), (p + r, q + s), (255, 0, 0), 2)
                        image = cv2.resize(image, (48, 48))
                        img = extract_features(image)
                        pred = emotion_model.predict(img)
                        prediction_label = labels[pred.argmax()]
                        cv2.putText(frame, '% s' % (prediction_label), (p - 10, q - 10),
                                    cv2.FONT_HERSHEY_COMPLEX_SMALL, 2, (0, 0, 255))
                except cv2.error:
                    pass

            cv2.imshow("Eye Controlled Mouse", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cam.release()
        cv2.destroyAllWindows()
        print("Game Ended")
    except Exception as e:
        print(f"Error: {str(e)}")

cam.release()
cv2.destroyAllWindows()
