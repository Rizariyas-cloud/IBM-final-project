import cv2
import numpy as np
import mediapipe as mp
import json
from tensorflow.keras.models import load_model
from collections import deque

# Load your pre-trained emotion classification model
model_path = 'emotion_recognition_model.keras'  # Replace with your model's path
emotion_model = load_model(model_path)

# Load emotion classes from saved file
with open('class_names.json', 'r') as f:
    emotion_labels = json.load(f)
print(f'Loaded emotion labels: {emotion_labels}')

# Initialize MediaPipe Face Mesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    static_image_mode=False,
    max_num_faces=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

# Initialize prediction smoothing
SMOOTHING_WINDOW = 5
prediction_queue = deque(maxlen=SMOOTHING_WINDOW)

def preprocess_face(face_roi):
    """Preprocess face image for the model"""
    try:
        # Convert to grayscale
        gray = cv2.cvtColor(face_roi, cv2.COLOR_BGR2GRAY)
        
        # Resize to model input size
        resized = cv2.resize(gray, (48, 48))
        
        # Normalize pixel values
        normalized = resized.astype('float32') / 255.0
        
        # Add required dimensions
        processed = np.expand_dims(normalized, axis=-1)
        processed = np.expand_dims(processed, axis=0)
        
        return processed
    except Exception as e:
        print(f"Error in preprocessing: {e}")
        return None

def get_face_bbox(landmarks, frame_shape):
    """Get face bounding box with padding"""
    try:
        h, w = frame_shape[:2]
        
        # Get all x and y coordinates
        x_coords = [int(landmark.x * w) for landmark in landmarks.landmark]
        y_coords = [int(landmark.y * h) for landmark in landmarks.landmark]
        
        # Calculate bounding box with padding
        padding = 30
        x_min = max(0, min(x_coords) - padding)
        y_min = max(0, min(y_coords) - padding)
        x_max = min(w, max(x_coords) + padding)
        y_max = min(h, max(y_coords) + padding)
        
        return x_min, y_min, x_max, y_max
    except Exception as e:
        print(f"Error in bbox calculation: {e}")
        return None

def smooth_predictions(current_prediction):
    """Smooth predictions using moving average"""
    try:
        prediction_queue.append(current_prediction)
        if len(prediction_queue) > 0:
            # Average the predictions
            avg_predictions = np.mean(prediction_queue, axis=0)
            return np.argmax(avg_predictions)
        return np.argmax(current_prediction)
    except Exception as e:
        print(f"Error in prediction smoothing: {e}")
        return None

# Start webcam capture
cap = cv2.VideoCapture(0)

while cap.isOpened():
    try:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break

        # Convert to RGB for MediaPipe
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(rgb_frame)

        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                # Get face bounding box
                bbox = get_face_bbox(face_landmarks, frame.shape)
                if bbox is None:
                    continue
                    
                x_min, y_min, x_max, y_max = bbox
                
                # Extract face ROI
                face_roi = frame[y_min:y_max, x_min:x_max]
                if face_roi.size == 0:
                    continue
                
                # Preprocess face
                processed_face = preprocess_face(face_roi)
                if processed_face is None:
                    continue
                
                # Get emotion prediction
                emotion_prediction = emotion_model.predict(processed_face, verbose=0)[0]
                
                # Smooth prediction
                smoothed_idx = smooth_predictions(emotion_prediction)
                if smoothed_idx is None:
                    continue
                
                # Get prediction confidence
                confidence = emotion_prediction[smoothed_idx]
                
                # Draw bounding box
                cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)
                
                # Display emotion and confidence
                emotion_text = f"{emotion_labels[smoothed_idx]}: {confidence:.2f}"
                cv2.putText(frame, emotion_text, (x_min, y_min - 10),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

        # Display the frame
        cv2.imshow('Emotion Recognition', frame)
        
        # Break loop with 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            
    except Exception as e:
        print(f"Error in main loop: {e}")
        continue

# Clean up
cap.release()
cv2.destroyAllWindows()