from facePoints import facePoints

model_path = "shape_predictor_68_face_landmarks.dat"

frontal_face_detector = dlib.get_frontal_face_detector()
face_landmark_detector = dlib.shape_predictor(model_path)

mouth_cascade = cv2.CascadeClassifier('models/face_detect/haarcascade_mcs_mouth.xml')