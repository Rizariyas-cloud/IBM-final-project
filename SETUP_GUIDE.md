# Emotion Recognition Setup Guide

## Quick Start

### 1. Train the Model (Fix "Only Happiness" Issue)

```bash
# Install required packages
pip install tensorflow scikit-learn opencv-python matplotlib

# Run the fixed training script
python change.py
```

**Key fixes applied:**
- ✅ Deterministic class mapping (sorted folder names)
- ✅ Dynamic output layer size (matches actual classes)
- ✅ Class balancing with sklearn weights
- ✅ Detailed evaluation metrics (confusion matrix, per-class accuracy)
- ✅ Saves `class_names.json` for consistent inference

### 2. Start the Backend API

```bash
# Install FastAPI dependencies
pip install -r api/requirements.txt

# Start the API server
cd api
python main.py
# OR
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

The API will be available at `http://127.0.0.1:8000`

### 3. Start the React Frontend

```bash
# Navigate to React app
cd Emoodle

# Install dependencies
npm install

# Create environment file
echo "VITE_API_URL=http://127.0.0.1:8000" > .env

# Start development server
npm run dev
```

The website will be available at `http://localhost:5173`

## What Was Fixed

### Training Issues Resolved:
1. **Non-deterministic labels**: `os.listdir()` order was random, causing label mismatch
2. **Wrong output size**: Model had 7 outputs but dataset only has 5 classes
3. **Class imbalance**: Happy class had 7x more samples than disgust
4. **No evaluation**: Added confusion matrix and per-class metrics

### Integration Features:
- ✅ File upload with preview
- ✅ Webcam capture
- ✅ Real-time emotion prediction
- ✅ Confidence scores and all predictions
- ✅ Beautiful responsive UI
- ✅ Error handling

## API Endpoints

- `GET /` - API info and available classes
- `GET /health` - Health check
- `POST /predict` - Upload image and get emotion prediction
- `GET /classes` - Get available emotion classes

## Expected Results

After training with the fixes:
- All emotions should be detected (not just happiness)
- Balanced accuracy across classes
- Detailed metrics showing per-class performance
- Working web interface with file upload and webcam

## Troubleshooting

**If still getting "only happiness":**
1. Check the confusion matrix output during training
2. Verify `class_names.json` contains all your classes
3. Ensure test images are properly preprocessed (48x48 grayscale)

**If API connection fails:**
1. Check `VITE_API_URL` in `.env` file
2. Ensure backend is running on port 8000
3. Check browser console for CORS errors



