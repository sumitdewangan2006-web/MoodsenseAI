"""
MoodSense AI - Model Training Script
====================================
Ye script emotion detection ke liye CNN model train karega
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Dense, Dropout, Flatten, BatchNormalization
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import ReduceLROnPlateau, EarlyStopping
from tensorflow.keras.utils import to_categorical
import os

# ============================================
# STEP 1: Dataset Load Karna
# ============================================
def load_fer2013_data(csv_path='data/fer2013.csv'):
    """
    FER-2013 dataset ko load karta hai
    
    Dataset format:
    - emotion: 0=Angry, 1=Disgust, 2=Fear, 3=Happy, 4=Sad, 5=Surprise, 6=Neutral
    - pixels: 48x48 grayscale image pixels (space-separated)
    - Usage: Training or PublicTest or PrivateTest
    """
    print("📂 Dataset load ho raha hai...")
    
    # CSV file read karo
    df = pd.read_csv(csv_path)
    
    # Pixels ko array mein convert karo
    pixels = df['pixels'].tolist()
    
    # Empty list banao images ke liye
    images = []
    
    # Har pixel string ko array mein convert karo
    for pixel_sequence in pixels:
        # Space se split karo aur integer mein convert karo
        image = [int(pixel) for pixel in pixel_sequence.split(' ')]
        # 48x48 shape mein reshape karo
        image = np.array(image).reshape(48, 48, 1)
        # Normalize karo (0-255 ko 0-1 mein)
        image = image / 255.0
        images.append(image)
    
    # Images ko numpy array mein convert karo
    images = np.array(images)
    
    # Labels extract karo
    labels = to_categorical(df['emotion'], num_classes=7)
    
    print(f"✅ Dataset loaded: {images.shape[0]} images")
    return images, labels

# ============================================
# STEP 2: CNN Model Architecture Banana
# ============================================
def create_emotion_model():
    """
    Simple but effective CNN model banata hai
    
    Architecture:
    - 4 Convolutional blocks (Conv2D + BatchNorm + MaxPooling + Dropout)
    - Flatten layer
    - 2 Dense layers with dropout
    - Output layer (7 emotions)
    """
    print("🧠 Model architecture bana rahe hain...")
    
    model = Sequential([
        # ========== Block 1 ==========
        # Pehli convolutional layer - 32 filters, 3x3 kernel
        Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=(48, 48, 1)),
        # Batch normalization - training ko stable banata hai
        BatchNormalization(),
        # Max pooling - image size reduce karta hai (24x24)
        MaxPooling2D(pool_size=(2, 2)),
        # Dropout - overfitting rokta hai
        Dropout(0.25),
        
        # ========== Block 2 ==========
        Conv2D(64, kernel_size=(3, 3), activation='relu'),
        BatchNormalization(),
        MaxPooling2D(pool_size=(2, 2)),
        Dropout(0.25),
        
        # ========== Block 3 ==========
        Conv2D(128, kernel_size=(3, 3), activation='relu'),
        BatchNormalization(),
        MaxPooling2D(pool_size=(2, 2)),
        Dropout(0.25),
        
        # ========== Block 4 ==========
        Conv2D(256, kernel_size=(3, 3), activation='relu'),
        BatchNormalization(),
        MaxPooling2D(pool_size=(2, 2)),
        Dropout(0.25),
        
        # ========== Flatten & Dense Layers ==========
        # 2D data ko 1D mein convert karo
        Flatten(),
        
        # Fully connected layer - 512 neurons
        Dense(512, activation='relu'),
        BatchNormalization(),
        Dropout(0.5),
        
        # Second dense layer - 256 neurons
        Dense(256, activation='relu'),
        BatchNormalization(),
        Dropout(0.5),
        
        # ========== Output Layer ==========
        # 7 emotions ke liye 7 neurons, softmax for probability
        Dense(7, activation='softmax')
    ])
    
    print("✅ Model architecture ready!")
    return model

# ============================================
# STEP 3: Model Training Karna
# ============================================
def train_model(csv_path='data/fer2013.csv', epochs=50, batch_size=64):
    """
    Model ko train karta hai aur save karta hai
    """
    
    # Data load karo
    X, y = load_fer2013_data(csv_path)
    
    # Train-Test split (80% training, 20% testing)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    print(f"📊 Training samples: {X_train.shape[0]}")
    print(f"📊 Testing samples: {X_test.shape[0]}")
    
    # Model banao
    model = create_emotion_model()
    
    # Model compile karo
    # Adam optimizer - fast aur efficient
    # categorical_crossentropy - multi-class classification ke liye
    model.compile(
        optimizer=Adam(learning_rate=0.0001),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    
    # Model summary dikhao
    model.summary()
    
    # Callbacks - training ko smart banate hain
    # 1. ReduceLROnPlateau - learning rate reduce karta hai jab improvement nahi ho
    reduce_lr = ReduceLROnPlateau(
        monitor='val_loss',
        factor=0.5,
        patience=5,
        min_lr=0.00001,
        verbose=1
    )
    
    # 2. EarlyStopping - training rok deta hai agar improvement nahi ho
    early_stop = EarlyStopping(
        monitor='val_loss',
        patience=10,
        restore_best_weights=True,
        verbose=1
    )
    
    print("🏋️ Training shuru ho rahi hai... (This will take time!)")
    
    # Model train karo
    history = model.fit(
        X_train, y_train,
        batch_size=batch_size,
        epochs=epochs,
        validation_data=(X_test, y_test),
        callbacks=[reduce_lr, early_stop],
        verbose=1
    )
    
    # Model evaluate karo
    print("\n📈 Model evaluation:")
    test_loss, test_accuracy = model.evaluate(X_test, y_test, verbose=0)
    print(f"Test Accuracy: {test_accuracy * 100:.2f}%")
    print(f"Test Loss: {test_loss:.4f}")
    
    # Model save karo
    os.makedirs('models', exist_ok=True)
    model.save('models/emotion_model.h5')
    print("💾 Model saved at: models/emotion_model.h5")
    
    # Training graphs plot karo
    plot_training_history(history)
    
    return model, history

# ============================================
# STEP 4: Training Graphs Banana
# ============================================
def plot_training_history(history):
    """
    Training accuracy aur loss ke graphs banata hai
    """
    plt.figure(figsize=(12, 4))
    
    # Accuracy graph
    plt.subplot(1, 2, 1)
    plt.plot(history.history['accuracy'], label='Training Accuracy')
    plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
    plt.title('Model Accuracy')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy')
    plt.legend()
    plt.grid(True)
    
    # Loss graph
    plt.subplot(1, 2, 2)
    plt.plot(history.history['loss'], label='Training Loss')
    plt.plot(history.history['val_loss'], label='Validation Loss')
    plt.title('Model Loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.legend()
    plt.grid(True)
    
    plt.tight_layout()
    plt.savefig('models/training_history.png')
    print("📊 Training graphs saved at: models/training_history.png")
    plt.show()

# ============================================
# MAIN EXECUTION
# ============================================
if __name__ == "__main__":
    print("=" * 50)
    print("🎭 MoodSense AI - Model Training")
    print("=" * 50)
    
    # Check if dataset exists
    if not os.path.exists('data/fer2013.csv'):
        print("❌ ERROR: fer2013.csv not found!")
        print("📥 Please download from: https://www.kaggle.com/datasets/msambare/fer2013")
        print("📁 Place it in: data/fer2013.csv")
    else:
        # Train the model
        model, history = train_model(
            csv_path='data/fer2013.csv',
            epochs=50,  # Zyada epochs = better accuracy (but takes more time)
            batch_size=64
        )
        print("\n✅ Training complete!")
        print("👉 Ab app.py run karo Streamlit app chalane ke liye")
