# Emoodle: Facial Emotion Recognition

Emoodle is a facial emotion recognition system built with Python and deep learning. It detects a face from a webcam feed and classifies the person's facial expression into emotions such as **happy, sad, angry, fear, surprise, disgust, and neutral**.

Developed as part of my **IBM internship**.

## Features

- Real-time face detection using OpenCV
- Facial landmark detection
- Facial emotion classification using a trained deep learning model
- Real-time webcam-based emotion recognition
- Displays the predicted emotion on the detected face
- Supports emotion recognition from facial expressions

## Dataset

The model was trained using the **FER2013 (Facial Expression Recognition 2013)** dataset.

The dataset is **not included in this repository** because of its size.

You can download the FER2013 dataset from Kaggle:

https://www.kaggle.com/datasets/msambare/fer2013

After downloading, place the dataset in the appropriate `data` folder in the project root.

Example:

```text
emotion_recognition/
├── data/
│   └── fer2013/
├── model/
├── main.py
├── requirements.txt
└── README.md
