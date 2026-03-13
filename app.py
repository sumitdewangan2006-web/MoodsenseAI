"""
MoodSense AI - Streamlit Web Application
========================================
Beautiful UI with webcam integration aur emotion-based suggestions
"""

import streamlit as st
import cv2
import numpy as np
from PIL import Image
import time
from emotion_detector import EmotionDetector, EMOTION_ACTIONS

# ============================================
# PAGE CONFIGURATION
# ============================================
st.set_page_config(
    page_title="MoodSense AI",
    page_icon="🎭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# CUSTOM CSS STYLING
# ============================================
st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    h1 {
        color: white;
        text-align: center;
        font-size: 3rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    h2, h3 {
        color: white;
    }
    .emotion-box {
        background: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin: 10px 0;
    }
    .suggestion-box {
        background: #f0f8ff;
        padding: 15px;
        border-left: 4px solid #667eea;
        border-radius: 5px;
        margin: 10px 0;
    }
    .stButton>button {
        width: 100%;
        background-color: #667eea;
        color: white;
        font-size: 18px;
        padding: 10px;
        border-radius: 10px;
        border: none;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .stButton>button:hover {
        background-color: #764ba2;
        transform: translateY(-2px);
    }
    </style>
""", unsafe_allow_html=True)

# ============================================
# SESSION STATE INITIALIZATION
# ============================================
if 'detector' not in st.session_state:
    st.session_state.detector = None
if 'webcam_running' not in st.session_state:
    st.session_state.webcam_running = False
if 'last_emotion' not in st.session_state:
    st.session_state.last_emotion = None
if 'emotion_history' not in st.session_state:
    st.session_state.emotion_history = []

# ============================================
# HELPER FUNCTIONS
# ============================================

@st.cache_resource
def load_detector():
    """
    Emotion detector ko cache ke saath load karta hai
    (Model ko baar baar load nahi karna padega)
    """
    try:
        detector = EmotionDetector('models/emotion_model.h5')
        return detector
    except Exception as e:
        st.error(f"❌ Model load nahi hua: {str(e)}")
        return None

def display_emotion_info(emotion_label, confidence):
    """
    Emotion information aur suggestions display karta hai
    """
    st.markdown("---")
    
    # Emotion display
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown(f"""
            <div class='emotion-box' style='text-align: center;'>
                <h2>Current Emotion</h2>
                <h1 style='font-size: 4rem; margin: 10px 0;'>{emotion_label}</h1>
                <p style='font-size: 1.2rem; color: #666;'>
                    Confidence: {confidence*100:.1f}%
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Get action suggestions
        action_info = EMOTION_ACTIONS.get(emotion_label, EMOTION_ACTIONS['Neutral 😐'])
        
        st.markdown(f"""
            <div class='emotion-box'>
                <h2>{action_info['title']}</h2>
                <p style='font-size: 1.1rem; color: #444;'>
                    {action_info['suggestion']}
                </p>
                <div class='suggestion-box'>
                    <pre style='font-size: 1rem; color: #333; white-space: pre-wrap;'>
{action_info['action']}
                    </pre>
                </div>
            </div>
        """, unsafe_allow_html=True)

def update_emotion_history(emotion_label):
    """
    Emotion history update karta hai (last 10 emotions)
    """
    st.session_state.emotion_history.append({
        'emotion': emotion_label,
        'time': time.strftime('%H:%M:%S')
    })
    
    # Keep only last 10 emotions
    if len(st.session_state.emotion_history) > 10:
        st.session_state.emotion_history.pop(0)

# ============================================
# MAIN APPLICATION
# ============================================

def main():
    """
    Main application function
    """
    
    # Title
    st.markdown("<h1>🎭 MoodSense AI</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: white;'>Emotion-Based Smart Assistant</h3>", unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("## 📋 About")
        st.info("""
        **MoodSense AI** detects your emotions in real-time 
        and provides personalized suggestions!
        
        **Features:**
        - 🎥 Live webcam emotion detection
        - 😊 7 emotions recognized
        - 💡 Smart action suggestions
        - 📊 Emotion history tracking
        """)
        
        st.markdown("## 🎯 Detected Emotions")
        emotions_list = """
        - 😄 Happy
        - 😢 Sad
        - 😡 Angry
        - 😐 Neutral
        - 😨 Fear
        - 😲 Surprise
        - 🤢 Disgust
        """
        st.markdown(emotions_list)
        
        st.markdown("## 📊 Recent History")
        if st.session_state.emotion_history:
            for item in reversed(st.session_state.emotion_history[-5:]):
                st.text(f"{item['time']} - {item['emotion']}")
        else:
            st.text("No emotions detected yet")
    
    # Main content area
    tab1, tab2, tab3 = st.tabs(["📷 Live Detection", "📖 How It Works", "⚙️ Troubleshooting"])
    
    with tab1:
        st.markdown("### 🎥 Webcam Emotion Detection")
        
        # Load detector
        if st.session_state.detector is None:
            with st.spinner("🔧 Loading emotion detection model..."):
                st.session_state.detector = load_detector()
        
        if st.session_state.detector is None:
            st.error("""
            ❌ **Model not found!**
            
            Please train the model first:
            1. Download FER-2013 dataset
            2. Run: `python train_model.py`
            3. Wait for training to complete
            4. Refresh this page
            """)
            return
        
        # Webcam control buttons
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            start_button = st.button("▶️ Start Webcam", key="start")
        with col2:
            stop_button = st.button("⏹️ Stop Webcam", key="stop")
        with col3:
            capture_button = st.button("📸 Capture Emotion", key="capture")
        
        # Handle button clicks
        if start_button:
            st.session_state.webcam_running = True
        
        if stop_button:
            st.session_state.webcam_running = False
        
        # Webcam frame placeholder
        frame_placeholder = st.empty()
        emotion_placeholder = st.empty()
        
        # Webcam loop
        if st.session_state.webcam_running:
            cap = cv2.VideoCapture(0)
            
            if not cap.isOpened():
                st.error("""
                ❌ **Webcam could not be opened!**
                
                Please check:
                - Webcam is connected
                - No other app is using webcam
                - Browser has camera permission
                """)
                st.session_state.webcam_running = False
                return
            
            # Success message
            st.success("✅ Webcam is running! Your emotion will be detected automatically.")
            
            # Frame counter for emotion detection (detect every 10 frames)
            frame_count = 0
            
            while st.session_state.webcam_running:
                ret, frame = cap.read()
                
                if not ret:
                    st.error("❌ Failed to read webcam frame")
                    break
                
                # Process frame every 10 frames (for performance)
                if frame_count % 10 == 0:
                    # Detect emotion
                    processed_frame, emotions = st.session_state.detector.process_frame(frame)
                    
                    # Convert BGR to RGB for Streamlit
                    frame_rgb = cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB)
                    
                    # Display frame
                    frame_placeholder.image(frame_rgb, channels="RGB", use_column_width=True)
                    
                    # Display emotion if detected
                    if emotions:
                        emotion_label = emotions[0]['emotion']
                        confidence = emotions[0]['confidence']
                        
                        # Update last emotion
                        st.session_state.last_emotion = (emotion_label, confidence)
                        
                        # Update history
                        update_emotion_history(emotion_label)
                        
                        # Display emotion info
                        with emotion_placeholder.container():
                            display_emotion_info(emotion_label, confidence)
                else:
                    # Just display frame without processing
                    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    frame_placeholder.image(frame_rgb, channels="RGB", use_column_width=True)
                
                frame_count += 1
                
                # Small delay
                time.sleep(0.03)
            
            # Release webcam
            cap.release()
            st.info("📷 Webcam stopped")
        
        # Capture mode (single frame analysis)
        elif capture_button:
            cap = cv2.VideoCapture(0)
            
            if not cap.isOpened():
                st.error("❌ Could not open webcam for capture")
                return
            
            # Read one frame
            ret, frame = cap.read()
            cap.release()
            
            if ret:
                # Process frame
                processed_frame, emotions = st.session_state.detector.process_frame(frame)
                
                # Convert to RGB
                frame_rgb = cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB)
                
                # Display
                frame_placeholder.image(frame_rgb, channels="RGB", use_column_width=True)
                
                if emotions:
                    emotion_label = emotions[0]['emotion']
                    confidence = emotions[0]['confidence']
                    
                    with emotion_placeholder.container():
                        display_emotion_info(emotion_label, confidence)
                else:
                    st.warning("😶 No face detected! Please ensure your face is visible.")
            else:
                st.error("❌ Failed to capture image")
    
    with tab2:
        st.markdown("""
        ### 🧠 How MoodSense AI Works
        
        #### 1️⃣ Face Detection
        - Webcam se real-time video capture hota hai
        - OpenCV's Haar Cascade algorithm faces detect karta hai
        - Grayscale conversion for better accuracy
        
        #### 2️⃣ Emotion Recognition
        - Detected face ko 48x48 pixels mein resize kiya jata hai
        - Pre-trained CNN model emotion predict karta hai
        - 7 emotions: Happy, Sad, Angry, Neutral, Fear, Surprise, Disgust
        
        #### 3️⃣ Smart Suggestions
        - Har emotion ke liye specific actions suggest kiye jate hain:
          - **Sad** → Uplifting music suggestions
          - **Angry** → Breathing exercises
          - **Happy** → Motivational quotes
          - **Fear** → Calming messages
          - **Neutral** → Productivity tips
          - **Surprise** → Positive reinforcement
        
        #### 4️⃣ Technology Stack
        - **Python** - Programming language
        - **OpenCV** - Face detection & webcam handling
        - **TensorFlow/Keras** - Deep learning model
        - **Streamlit** - Beautiful web interface
        - **CNN Architecture** - 4 convolutional blocks + dense layers
        """)
    
    with tab3:
        st.markdown("""
        ### 🔧 Troubleshooting Guide
        
        #### ❌ Webcam Not Opening
        **Solution:**
        1. Check if webcam is physically connected
        2. Close other apps using webcam (Zoom, Teams, etc.)
        3. Grant browser permission to access camera
        4. Try running: `python emotion_detector.py` to test webcam
        5. On Windows, try running Command Prompt as Administrator
        
        #### ❌ Model Not Found Error
        **Solution:**
        1. Download FER-2013 dataset from Kaggle
        2. Place `fer2013.csv` in `data/` folder
        3. Run training script: `python train_model.py`
        4. Wait 30-60 minutes for training
        5. Check if `models/emotion_model.h5` exists
        
        #### ❌ No Face Detected
        **Solution:**
        1. Ensure good lighting in room
        2. Face camera directly
        3. Remove sunglasses or face masks
        4. Move closer to webcam
        5. Check if face is within frame
        
        #### ❌ Low Accuracy
        **Solution:**
        1. Train model for more epochs (50-100)
        2. Ensure proper lighting
        3. Use neutral expressions initially
        4. Avoid extreme angles
        
        #### ❌ Slow Performance
        **Solution:**
        1. Close other applications
        2. Reduce frame processing rate (in code)
        3. Use smaller model or GPU acceleration
        
        #### 📧 Still Having Issues?
        - Check Python version (3.8+ recommended)
        - Update packages: `pip install --upgrade -r requirements.txt`
        - Verify all files are in correct folders
        """)
    
    # Footer
    st.markdown("---")
    st.markdown("""
        <div style='text-align: center; color: white; padding: 20px;'>
            <p>Made with ❤️ using Python, TensorFlow & Streamlit</p>
            <p>🎭 MoodSense AI - Understanding emotions, one smile at a time</p>
        </div>
    """, unsafe_allow_html=True)

# ============================================
# RUN APPLICATION
# ============================================
if __name__ == "__main__":
    main()
