# 🎭 MoodSense AI - Emotion-Based Smart Assistant

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.15-orange.svg)
![OpenCV](https://img.shields.io/badge/OpenCV-4.8-green.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28-red.svg)

Real-time emotion detection web application jo aapke facial expressions se emotions detect karke personalized suggestions deta hai!

## 🌟 Features

- 🎥 **Real-time Webcam Detection** - Live emotion detection
- 😊 **7 Emotions Recognized** - Happy, Sad, Angry, Neutral, Fear, Surprise, Disgust
- 💡 **Smart Suggestions** - Emotion-based personalized actions
- 📊 **Emotion History** - Track your emotional journey
- 🎨 **Beautiful UI** - Gradient design with smooth animations
- 🚀 **Easy to Use** - Beginner-friendly interface

## 📸 Screenshots

```
[Webcam View] → [Face Detection] → [Emotion Prediction] → [Smart Suggestion]
    😊              🔍                   😄                    💡
```

## 🛠️ Technology Stack

| Technology | Purpose |
|------------|---------|
| Python 3.8+ | Programming Language |
| TensorFlow/Keras | Deep Learning Framework |
| OpenCV | Face Detection & Webcam |
| Streamlit | Web Application Framework |
| NumPy | Numerical Computing |
| FER-2013 | Training Dataset |

## 📋 Prerequisites

- Windows 10/11 (or Linux/Mac)
- Python 3.8 or higher
- Webcam (built-in or external)
- 4GB RAM minimum
- Internet connection (for initial setup)

## 🚀 Installation Guide (Windows)

### Step 1: Clone or Download Project

```bash
# Option 1: Clone repository (if using Git)
git clone https://github.com/yourusername/moodsense-ai.git
cd moodsense-ai

# Option 2: Download ZIP and extract
# Then open Command Prompt in project folder
```

### Step 2: Create Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# On Mac/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
# Install all required packages
pip install -r requirements.txt

# If you get errors, try:
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 4: Download Dataset

1. Go to: https://www.kaggle.com/datasets/msambare/fer2013
2. Download `fer2013.csv` file (about 100MB)
3. Create `data` folder in project directory
4. Place `fer2013.csv` inside `data/` folder

```
Project Structure:
MoodSense-AI/
├── data/
│   └── fer2013.csv  ← Place here
```

### Step 5: Train the Model

```bash
# Run training script (This will take 30-60 minutes)
python train_model.py

# What happens:
# - Loads dataset
# - Trains CNN model
# - Saves model to models/emotion_model.h5
# - Shows training graphs
```

**Training Output Example:**
```
📂 Dataset load ho raha hai...
✅ Dataset loaded: 35887 images
🧠 Model architecture bana rahe hain...
📊 Training samples: 28709
📊 Testing samples: 7178
🏋️ Training shuru ho rahi hai...
Epoch 1/50
...
💾 Model saved at: models/emotion_model.h5
```

### Step 6: Test Webcam (Optional but Recommended)

```bash
# Test if webcam works correctly
python emotion_detector.py

# Press 'q' to quit
```

### Step 7: Run Web Application

```bash
# Start Streamlit app
streamlit run app.py

# App will open in browser automatically at:
# http://localhost:8501
```

## 🎮 How to Use

1. **Start Application**
   ```bash
   streamlit run app.py
   ```

2. **Open in Browser**
   - App opens automatically at `http://localhost:8501`
   - If not, manually open this URL

3. **Grant Camera Permission**
   - Browser will ask for camera access
   - Click "Allow"

4. **Start Detection**
   - Click "▶️ Start Webcam" button
   - Position your face in front of camera
   - Emotion will be detected automatically

5. **View Suggestions**
   - Detected emotion appears on right side
   - Smart suggestions based on your emotion
   - History shows in sidebar

## 😊 Emotion → Action Mapping

| Emotion | Suggestion | Action |
|---------|-----------|--------|
| 😄 Happy | Keep spreading positivity | Motivational Quote |
| 😢 Sad | This too shall pass | Uplifting Song Suggestions |
| 😡 Angry | Take a deep breath | Breathing Exercise Steps |
| 😐 Neutral | Boost productivity | Productivity Tips |
| 😨 Fear | You're safe | Calming Message |
| 😲 Surprise | Embrace the unexpected | Fun Positive Message |
| 🤢 Disgust | Refresh yourself | Take a Break Tip |

## 📁 Project Structure

```
MoodSense-AI/
│
├── data/
│   └── fer2013.csv              # FER-2013 dataset
│
├── models/
│   ├── emotion_model.h5         # Trained model (after training)
│   └── training_history.png     # Training graphs
│
├── venv/                        # Virtual environment (created by you)
│
├── train_model.py               # Model training script
├── emotion_detector.py          # Emotion detection logic
├── app.py                       # Streamlit web application
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

## 🧠 Model Architecture

```
CNN Architecture:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Input: 48x48x1 (Grayscale Image)
│
├── Conv Block 1 (32 filters)
│   ├── Conv2D + ReLU
│   ├── BatchNormalization
│   ├── MaxPooling2D
│   └── Dropout (25%)
│
├── Conv Block 2 (64 filters)
│   ├── Conv2D + ReLU
│   ├── BatchNormalization
│   ├── MaxPooling2D
│   └── Dropout (25%)
│
├── Conv Block 3 (128 filters)
│   ├── Conv2D + ReLU
│   ├── BatchNormalization
│   ├── MaxPooling2D
│   └── Dropout (25%)
│
├── Conv Block 4 (256 filters)
│   ├── Conv2D + ReLU
│   ├── BatchNormalization
│   ├── MaxPooling2D
│   └── Dropout (25%)
│
├── Flatten Layer
│
├── Dense Layer (512 neurons)
│   ├── ReLU activation
│   ├── BatchNormalization
│   └── Dropout (50%)
│
├── Dense Layer (256 neurons)
│   ├── ReLU activation
│   ├── BatchNormalization
│   └── Dropout (50%)
│
└── Output Layer (7 neurons)
    └── Softmax activation

Total Parameters: ~5 million
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## 🔧 Troubleshooting

### ❌ Problem: Webcam Not Opening

**Solutions:**
```bash
# 1. Check if webcam is detected
python -c "import cv2; print('Webcams:', [cv2.VideoCapture(i).isOpened() for i in range(3)])"

# 2. Close other apps using webcam (Zoom, Teams, Skype)

# 3. Check camera permissions in Windows Settings:
# Settings → Privacy → Camera → Allow apps to access camera

# 4. Try different camera index in code:
# Change: cap = cv2.VideoCapture(0)
# To: cap = cv2.VideoCapture(1)
```

### ❌ Problem: Model Not Found Error

**Solutions:**
```bash
# Check if model exists
dir models

# If not, train the model:
python train_model.py

# Expected output file:
# models/emotion_model.h5
```

### ❌ Problem: ImportError or ModuleNotFoundError

**Solutions:**
```bash
# Reinstall all packages
pip uninstall -r requirements.txt -y
pip install -r requirements.txt

# Or install individually:
pip install opencv-python tensorflow streamlit numpy pandas matplotlib scikit-learn
```

### ❌ Problem: TensorFlow Installation Failed

**Solutions:**
```bash
# For Windows (if normal install fails):
pip install tensorflow-cpu

# For Mac with M1/M2 chip:
pip install tensorflow-macos tensorflow-metal

# Check installation:
python -c "import tensorflow as tf; print(tf.__version__)"
```

### ❌ Problem: Face Not Detected

**Checklist:**
- ✅ Good lighting in room
- ✅ Face directly toward camera
- ✅ Remove sunglasses/mask
- ✅ Distance: 1-3 feet from camera
- ✅ Camera lens is clean

### ❌ Problem: Low Accuracy

**Solutions:**
1. Train for more epochs (50-100 instead of 30)
2. Add data augmentation
3. Ensure proper lighting during testing
4. Calibrate with neutral expression first

### ❌ Problem: Streamlit Not Opening

**Solutions:**
```bash
# 1. Check if Streamlit is installed
streamlit --version

# 2. Manually open browser to:
http://localhost:8501

# 3. Change port if 8501 is busy:
streamlit run app.py --server.port 8502

# 4. Check firewall settings
```

### ❌ Problem: Slow Performance

**Solutions:**
1. Close unnecessary applications
2. Reduce frame processing rate in code
3. Use GPU if available (install `tensorflow-gpu`)
4. Lower webcam resolution

## 📊 Expected Training Results

After training, you should see approximately:

| Metric | Value |
|--------|-------|
| Training Accuracy | 65-75% |
| Validation Accuracy | 60-70% |
| Training Loss | 0.8-1.0 |
| Validation Loss | 0.9-1.2 |
| Training Time | 30-60 minutes |

*Note: FER-2013 is a challenging dataset. 60-70% accuracy is considered good!*

## 🎯 Tips for Best Results

### For Better Detection:
1. 💡 **Good Lighting** - Face should be well-lit
2. 📐 **Front-Facing** - Look directly at camera
3. 😊 **Clear Expression** - Make distinct facial expressions
4. 🎥 **Stable Position** - Keep face steady in frame
5. 🧹 **Clean Background** - Avoid cluttered backgrounds

### For Better Training:
1. ⏰ **Be Patient** - Training takes 30-60 minutes
2. 🔄 **More Epochs** - 50+ epochs for better accuracy
3. 💾 **Save Checkpoints** - Model saves automatically
4. 📊 **Monitor Graphs** - Check training_history.png
5. 🎮 **GPU Recommended** - Much faster training (optional)

## 🎓 Learning Resources

### Understanding CNN:
- Convolutional layers detect features (edges, shapes, patterns)
- Pooling layers reduce size while keeping important info
- Dense layers make final emotion decision
- Dropout prevents overfitting (memorizing training data)

### Key Concepts:
- **Epoch** - One complete pass through entire dataset
- **Batch Size** - Number of images processed at once
- **Learning Rate** - How fast model learns
- **Accuracy** - Percentage of correct predictions
- **Loss** - How wrong the predictions are (lower is better)

## 🤝 Contributing

Found a bug? Have a suggestion? Feel free to:
1. Open an issue
2. Submit a pull request
3. Share your improvements

## 📝 License

This project is open source and available for educational purposes.

## 🙏 Acknowledgments

- **FER-2013 Dataset** - Kaggle
- **OpenCV** - Face detection
- **TensorFlow Team** - Deep learning framework
- **Streamlit** - Beautiful web framework

## 📧 Support

Having issues? 

1. **Check Troubleshooting Section** in README
2. **Review Code Comments** - Detailed Hinglish explanations
3. **Run Test Script** - `python emotion_detector.py`
4. **Check Console Errors** - Read error messages carefully

## 🎉 Success Checklist

Before considering project complete:

- [ ] Dataset downloaded and placed in `data/` folder
- [ ] Virtual environment created and activated
- [ ] All packages installed successfully
- [ ] Model trained (`emotion_model.h5` exists)
- [ ] Webcam test successful (`emotion_detector.py`)
- [ ] Streamlit app runs without errors
- [ ] Face detection works in browser
- [ ] Emotions are detected correctly
- [ ] Suggestions appear based on emotions
- [ ] You've tested all 7 emotions! 😊

## 🚀 Next Steps / Improvements

Want to make it better? Try:

1. **Add More Emotions** - Train with more emotion categories
2. **Music Integration** - Actually play songs using Spotify API
3. **Voice Commands** - Add speech recognition
4. **Mobile App** - Convert to mobile using React Native
5. **Emotion Journal** - Save emotion history to database
6. **Multi-Face Detection** - Detect multiple people's emotions
7. **Real-time Analytics** - Graphs of emotion trends over time
8. **Export Reports** - PDF reports of emotion patterns

## 📅 Version History

- **v1.0** (2024) - Initial release
  - Basic emotion detection
  - 7 emotions supported
  - Streamlit web interface
  - Hinglish comments

---

<div align="center">

**Made with ❤️ for College Students**

🎭 Understanding emotions, one smile at a time 😊

*Happy Coding!* 🚀

</div>
