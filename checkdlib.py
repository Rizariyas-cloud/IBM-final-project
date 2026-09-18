import os
import numpy as np
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.models import Sequential
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint

# Paths for FER2013 dataset
train_path = r"C:\Users\HP\OneDrive\Desktop\EMoBhool\fer213\train"
test_path = r"C:\Users\HP\OneDrive\Desktop\EMoBhool\fer213\test"

# Parameters
IMG_SIZE = (128, 128)  # Reduced image size for speed
BATCH_SIZE = 32
EPOCHS = 30  # Fewer epochs for faster training

# Data Generator with Augmentation
datagen = ImageDataGenerator(
    rescale=1.0/255.0,
    rotation_range=5,  # Simplified augmentation
    width_shift_range=0.05,
    height_shift_range=0.05,
    horizontal_flip=True
)

train_gen = datagen.flow_from_directory(
    train_path,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='categorical'
)

val_gen = datagen.flow_from_directory(
    test_path,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='categorical'
)

# Load Pretrained Model (MobileNetV2)
base_model = MobileNetV2(weights='imagenet', include_top=False, input_shape=(128, 128, 3))

# Build Model
model = Sequential([
    base_model,
    GlobalAveragePooling2D(),
    Dense(256, activation='relu'),  # Reduced dense units
    Dropout(0.3),  # Reduced dropout
    Dense(7, activation='softmax')  # 7 classes for FER2013
])

# Freeze the base model
for layer in base_model.layers:
    layer.trainable = False

# Compile Model
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Callbacks
callbacks = [
    EarlyStopping(patience=5, monitor='val_loss', restore_best_weights=True),
    ModelCheckpoint('best_light_emotion_model.keras', save_best_only=True, monitor='val_loss')
]

# Train the model
history = model.fit(
    train_gen,
    validation_data=val_gen,
    epochs=EPOCHS,
    callbacks=callbacks
)

# Save the model
model.save('light_emotion_model.keras')
print("Model saved successfully!")

# Evaluate the model
loss, accuracy = model.evaluate(val_gen)
print(f'Test Loss: {loss}, Test Accuracy: {accuracy}')
