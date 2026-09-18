import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import cv2
import numpy as np
import matplotlib.pyplot as plt
import json
from sklearn.model_selection import train_test_split
from sklearn.utils.class_weight import compute_class_weight
from sklearn.metrics import classification_report, confusion_matrix
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout, BatchNormalization
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import tensorflow as tf

# Paths for training and testing datasets
train_path = r"C:\Users\HP\OneDrive\Desktop\EMoBhool\fer213\train"
test_path = r"C:\Users\HP\OneDrive\Desktop\EMoBhool\fer213\test"

# Define deterministic class order (sorted)
class_names = sorted(os.listdir(train_path))
print(f'Class names (sorted): {class_names}')
print(f'Number of classes: {len(class_names)}')

# Verify test path has same classes
test_classes = sorted(os.listdir(test_path))
if class_names != test_classes:
    print(f'WARNING: Train classes {class_names} != Test classes {test_classes}')
    print('Using train classes only')

# Save class names for inference
with open('class_names.json', 'w') as f:
    json.dump(class_names, f)

# Confirm data directories
print(f'Train folders: {os.listdir(train_path)}')
print(f'Test folders: {os.listdir(test_path)}')

def load_data(data_path, class_names):
    X, y = [], []
    
    for emotion in class_names:
        emotion_folder = os.path.join(data_path, emotion)
        if not os.path.exists(emotion_folder):
            print(f"Warning: {emotion_folder} does not exist")
            continue
            
        label = class_names.index(emotion)
        img_count = 0
        
        for img_name in os.listdir(emotion_folder):
            img_path = os.path.join(emotion_folder, img_name)
            img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
            if img is None:
                continue
            img = cv2.resize(img, (48, 48))

            X.append(img)
            y.append(label)
            img_count += 1
        
        print(f'{emotion}: {img_count} images')

    X = np.array(X).astype('float32') / 255.0
    X = np.expand_dims(X, -1)  # Adding channel dimension
    y = np.array(y)
    
    return X, y

# Load the train and test data
X_train, y_train = load_data(train_path, class_names)
X_test, y_test = load_data(test_path, class_names)

# Compute class weights for imbalanced dataset
class_weights = compute_class_weight(
    class_weight='balanced',
    classes=np.unique(y_train),
    y=y_train
)
class_weight_dict = {i: class_weights[i] for i in range(len(class_names))}
print(f'Class weights: {class_weight_dict}')

# Data augmentation to improve generalization
datagen = ImageDataGenerator(
    rotation_range=10,
    width_shift_range=0.1,
    height_shift_range=0.1,
    horizontal_flip=True
)
datagen.fit(X_train)

# Enhanced model architecture
model = Sequential([
    Conv2D(64, (3, 3), activation='relu', input_shape=(48, 48, 1)),
    BatchNormalization(),
    MaxPooling2D((2, 2)),
    Dropout(0.3),

    Conv2D(128, (3, 3), activation='relu'),
    BatchNormalization(),
    MaxPooling2D((2, 2)),
    Dropout(0.4),

    Conv2D(256, (3, 3), activation='relu'),
    BatchNormalization(),
    MaxPooling2D((2, 2)),
    Dropout(0.4),

    Conv2D(256, (3, 3), activation='relu'),
    BatchNormalization(),
    MaxPooling2D((2, 2)),
    Dropout(0.5),

    Flatten(),
    Dense(256, activation='relu'),
    BatchNormalization(),
    Dropout(0.5),
    
    Dense(len(class_names), activation='softmax')
])

print(f'Model output layer size: {len(class_names)} (should match dataset classes)')

# Compile the model
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# Early stopping to prevent overfitting and save the best model
callbacks = [
    EarlyStopping(patience=10, monitor='val_loss', restore_best_weights=True),
    ModelCheckpoint('best_model.keras', save_best_only=True, monitor='val_loss')
]

# Train the model with data augmentation and class weights
history = model.fit(
    datagen.flow(X_train, y_train, batch_size=32),
    validation_data=(X_test, y_test),
    epochs=50,
    callbacks=callbacks,
    class_weight=class_weight_dict
)

# Evaluate the model
loss, accuracy = model.evaluate(X_test, y_test)
print(f'Test Loss: {loss}, Test Accuracy: {accuracy}')

# Get predictions for detailed evaluation
y_pred = model.predict(X_test)
y_pred_classes = np.argmax(y_pred, axis=1)

# Print classification report
print("\nClassification Report:")
print(classification_report(y_test, y_pred_classes, target_names=class_names))

# Print confusion matrix
print("\nConfusion Matrix:")
cm = confusion_matrix(y_test, y_pred_classes)
print(cm)

# Print per-class accuracy
print("\nPer-class accuracy:")
for i, class_name in enumerate(class_names):
    class_mask = y_test == i
    if np.sum(class_mask) > 0:
        class_acc = np.sum((y_pred_classes[class_mask] == i)) / np.sum(class_mask)
        print(f'{class_name}: {class_acc:.3f}')

model.save('emotion_recognition_model.keras')
print("Model saved successfully!")

loaded_model = tf.keras.models.load_model('emotion_recognition_model.keras')

def plot_image(index, predictions_array, true_label, img):
    plt.grid(False)
    plt.xticks([])
    plt.yticks([])
    plt.imshow(img[index], cmap='gray')

    predicted_label = np.argmax(predictions_array[index])
    color = 'blue' if predicted_label == true_label[index] else 'red'

    plt.xlabel(f"Pred: {class_names[predicted_label]}, True: {class_names[true_label[index]]}", color=color)

# Make predictions
predictions = model.predict(X_test)

# Plot a few test images with predictions
plt.figure(figsize=(10, 10))
for i in range(9):
    plt.subplot(3, 3, i + 1)
    plot_image(i, predictions, y_test, X_test)
plt.show()


