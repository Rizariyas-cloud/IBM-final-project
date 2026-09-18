from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from tensorflow.keras.models import load_model
import numpy as np
import cv2
import json
import io
from PIL import Image
import os

app = FastAPI(title="Emotion Recognition API", version="1.0.0")

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load model and class names on startup
model = None
class_names = None

@app.on_event("startup")
async def startup_event():
    global model, class_names
    
    # Resolve paths relative to project root (one level up from api/)
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    model_path = os.path.join(base_dir, "emotion_recognition_model.keras")
    class_names_path = os.path.join(base_dir, "class_names.json")
    
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found: {model_path}")
    if not os.path.exists(class_names_path):
        raise FileNotFoundError(f"Class names file not found: {class_names_path}")
    
    model = load_model(model_path)
    with open(class_names_path, 'r') as f:
        class_names = json.load(f)
    
    print(f"Model loaded successfully from {model_path}")
    print(f"Classes loaded from {class_names_path}: {class_names}")

def preprocess_image(image_bytes):
    """Preprocess image for emotion recognition model"""
    try:
        # Convert bytes to PIL Image
        pil_image = Image.open(io.BytesIO(image_bytes))
        
        # Convert to grayscale
        if pil_image.mode != 'L':
            pil_image = pil_image.convert('L')
        
        # Convert to numpy array
        img_array = np.array(pil_image)
        
        # Resize to model input size (48x48)
        img_resized = cv2.resize(img_array, (48, 48))
        
        # Normalize pixel values to 0-1
        img_normalized = img_resized.astype('float32') / 255.0
        
        # Add required dimensions: (1, 48, 48, 1)
        img_processed = np.expand_dims(img_normalized, axis=-1)
        img_processed = np.expand_dims(img_processed, axis=0)
        
        return img_processed
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Image preprocessing failed: {str(e)}")

@app.get("/")
async def root():
    return {"message": "Emotion Recognition API", "classes": class_names}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "model_loaded": model is not None}

@app.post("/predict")
async def predict_emotion(file: UploadFile = File(...)):
    """
    Predict emotion from uploaded image
    """
    if model is None or class_names is None:
        raise HTTPException(status_code=500, detail="Model not loaded")
    
    # Validate file type
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    try:
        # Read image bytes
        image_bytes = await file.read()
        
        # Preprocess image
        processed_image = preprocess_image(image_bytes)
        
        # Make prediction
        predictions = model.predict(processed_image, verbose=0)[0]
        
        # Get predicted class and confidence
        predicted_class_idx = int(np.argmax(predictions))
        confidence = float(predictions[predicted_class_idx])
        predicted_class = class_names[predicted_class_idx]
        
        # Get all class probabilities
        all_predictions = {
            class_names[i]: float(predictions[i]) 
            for i in range(len(class_names))
        }
        
        return {
            "predicted_emotion": predicted_class,
            "confidence": confidence,
            "all_predictions": all_predictions,
            "class_index": predicted_class_idx
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

@app.get("/classes")
async def get_classes():
    """Get available emotion classes"""
    return {"classes": class_names}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
