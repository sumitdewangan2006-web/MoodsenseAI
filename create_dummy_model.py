"""
MoodSense AI - Simple Pre-trained Model Creator
===============================================
Agar aapke paas FER-2013 dataset nahi hai, to ye script
ek simple pre-trained model create kar dega jo basic emotions
detect kar sakta hai.

NOTE: Ye model training se kam accurate hoga, but testing ke liye kaafi hai!
"""

import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Dense, Dropout, Flatten, BatchNormalization
import os

def create_simple_pretrained_model():
    """
    Ek simple CNN model banata hai with random weights
    Testing purposes ke liye
    
    NOTE: Ye model properly trained nahi hai!
    Real accuracy ke liye train_model.py use karo
    """
    
    print("=" * 50)
    print("🎭 Creating Simple Pre-trained Model")
    print("=" * 50)
    print()
    
    print("⚠️  WARNING: Ye model randomly initialized hai!")
    print("⚠️  Real accuracy ke liye proper training zaruri hai!")
    print()
    
    # Same architecture as training script
    model = Sequential([
        # Block 1
        Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=(48, 48, 1)),
        BatchNormalization(),
        MaxPooling2D(pool_size=(2, 2)),
        Dropout(0.25),
        
        # Block 2
        Conv2D(64, kernel_size=(3, 3), activation='relu'),
        BatchNormalization(),
        MaxPooling2D(pool_size=(2, 2)),
        Dropout(0.25),
        
        # Block 3
        Conv2D(128, kernel_size=(3, 3), activation='relu'),
        BatchNormalization(),
        MaxPooling2D(pool_size=(2, 2)),
        Dropout(0.25),
        
        # Block 4
        Conv2D(256, kernel_size=(3, 3), activation='relu'),
        BatchNormalization(),
        MaxPooling2D(pool_size=(2, 2)),
        Dropout(0.25),
        
        # Dense layers
        Flatten(),
        Dense(512, activation='relu'),
        BatchNormalization(),
        Dropout(0.5),
        Dense(256, activation='relu'),
        BatchNormalization(),
        Dropout(0.5),
        
        # Output
        Dense(7, activation='softmax')
    ])
    
    # Compile model
    model.compile(
        optimizer='adam',
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    
    # Create models directory
    os.makedirs('models', exist_ok=True)
    
    # Save model
    model.save('models/emotion_model.h5')
    
    print("✅ Model created and saved!")
    print("📁 Location: models/emotion_model.h5")
    print()
    print("📝 Important Notes:")
    print("   1. Ye model trained NAHI hai")
    print("   2. Random predictions dega initially")
    print("   3. Testing ke liye theek hai")
    print("   4. Production use ke liye train_model.py run karo")
    print()
    print("🚀 Ab aap app.py run kar sakte ho:")
    print("   streamlit run app.py")
    print()

if __name__ == "__main__":
    create_simple_pretrained_model()
