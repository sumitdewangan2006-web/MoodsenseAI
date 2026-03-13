"""
MoodSense AI - Emotion Detection Logic
======================================
Ye script webcam se face detect karega aur emotion predict karega
"""

import cv2
import numpy as np
from tensorflow.keras.models import load_model
import os

# ============================================
# Emotion Labels (FER-2013 dataset order)
# ============================================
EMOTION_LABELS = {
    0: 'Angry 😡',
    1: 'Disgust 🤢',
    2: 'Fear 😨',
    3: 'Happy 😄',
    4: 'Sad 😢',
    5: 'Surprise 😲',
    6: 'Neutral 😐'
}

# ============================================
# Emotion-Based Action Suggestions
# ============================================
EMOTION_ACTIONS = {
    'Happy 😄': {
        'title': '🌟 You\'re feeling great!',
        'suggestion': 'Keep spreading positivity! Share your happiness with others.',
        'action': '💡 Motivational Quote:\n"The purpose of our lives is to be happy." - Dalai Lama'
    },
    'Sad 😢': {
        'title': '💙 We understand you\'re feeling down',
        'suggestion': 'It\'s okay to feel sad. Remember, this too shall pass.',
        'action': '🎵 Song Suggestion:\n"Here Comes The Sun" by The Beatles\n"Happy" by Pharrell Williams'
    },
    'Angry 😡': {
        'title': '🔥 Take a deep breath',
        'suggestion': 'Anger is natural. Let\'s calm down together.',
        'action': '🧘 Breathing Exercise:\n1. Breathe in for 4 seconds\n2. Hold for 4 seconds\n3. Breathe out for 6 seconds\n4. Repeat 5 times'
    },
    'Neutral 😐': {
        'title': '⚡ Time to boost your productivity!',
        'suggestion': 'You seem calm and focused. Perfect time for work!',
        'action': '📝 Productivity Tip:\n"Break your tasks into smaller chunks. Complete one thing at a time."'
    },
    'Fear 😨': {
        'title': '🤗 You\'re safe here',
        'suggestion': 'Whatever you\'re worried about, you can overcome it.',
        'action': '💪 Calming Message:\n"Fear is temporary. Courage is forever. You\'ve got this!"'
    },
    'Surprise 😲': {
        'title': '✨ Something surprised you!',
        'suggestion': 'Life is full of surprises. Embrace the unexpected!',
        'action': '🎉 Fun Message:\n"Surprises are the spice of life! Keep that excitement going!"'
    },
    'Disgust 🤢': {
        'title': '😊 Let\'s shift your mood',
        'suggestion': 'Something bothering you? Take a break and refresh.',
        'action': '🌿 Tip:\n"Step outside for fresh air or listen to your favorite music."'
    }
}

# ============================================
# CLASS: EmotionDetector
# ============================================
class EmotionDetector:
    """
    Main class jo face detection aur emotion prediction handle karta hai
    """
    
    def __init__(self, model_path='models/emotion_model.h5'):
        """
        Constructor - model aur face detector load karta hai
        """
        print("🔧 Initializing Emotion Detector...")
        
        # Check if model file exists
        if not os.path.exists(model_path):
            raise FileNotFoundError(
                f"❌ Model file not found at: {model_path}\n"
                f"👉 Please train the model first using train_model.py"
            )
        
        # Load trained emotion detection model
        print("📦 Loading emotion detection model...")
        self.model = load_model(model_path)
        print("✅ Model loaded successfully!")
        
        # Load Haar Cascade for face detection
        # Ye pre-trained classifier hai jo faces detect karta hai
        print("👤 Loading face detection classifier...")
        cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        self.face_cascade = cv2.CascadeClassifier(cascade_path)
        
        if self.face_cascade.empty():
            raise Exception("❌ Could not load face detection classifier!")
        
        print("✅ Face detector loaded successfully!")
        
    def detect_faces(self, frame):
        """
        Frame mein faces detect karta hai
        
        Args:
            frame: Input image/video frame
            
        Returns:
            faces: List of detected face coordinates (x, y, w, h)
        """
        # Convert image to grayscale (face detection grayscale mein better work karta hai)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Detect faces
        # Parameters:
        # - scaleFactor: Image size ko kitna reduce karein (1.3 = 30% reduction per scan)
        # - minNeighbors: Kitne neighboring detections chahiye confirmation ke liye
        # - minSize: Minimum face size
        faces = self.face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.3,
            minNeighbors=5,
            minSize=(30, 30)
        )
        
        return faces, gray
    
    def predict_emotion(self, face_roi):
        """
        Face region se emotion predict karta hai
        
        Args:
            face_roi: Cropped face region (grayscale)
            
        Returns:
            emotion_label: Predicted emotion (string)
            confidence: Prediction confidence (0-1)
        """
        # Face ko 48x48 size mein resize karo (model input size)
        face_resized = cv2.resize(face_roi, (48, 48))
        
        # Normalize karo (0-255 ko 0-1 mein)
        face_normalized = face_resized / 255.0
        
        # Shape add karo for model input: (1, 48, 48, 1)
        # 1st dimension: batch size
        # Last dimension: grayscale channel
        face_input = face_normalized.reshape(1, 48, 48, 1)
        
        # Model se prediction lo
        prediction = self.model.predict(face_input, verbose=0)
        
        # Highest probability wala emotion nikalo
        emotion_idx = np.argmax(prediction[0])
        confidence = prediction[0][emotion_idx]
        
        # Emotion label get karo
        emotion_label = EMOTION_LABELS[emotion_idx]
        
        return emotion_label, confidence
    
    def get_emotion_action(self, emotion_label):
        """
        Emotion ke basis pe suggested action return karta hai
        
        Args:
            emotion_label: Detected emotion
            
        Returns:
            action_dict: Dictionary with title, suggestion, and action
        """
        return EMOTION_ACTIONS.get(emotion_label, EMOTION_ACTIONS['Neutral 😐'])
    
    def process_frame(self, frame):
        """
        Complete frame processing:
        1. Face detection
        2. Emotion prediction
        3. Draw rectangles and labels
        
        Args:
            frame: Input video frame
            
        Returns:
            processed_frame: Frame with annotations
            detected_emotions: List of detected emotions
        """
        # Faces detect karo
        faces, gray = self.detect_faces(frame)
        
        detected_emotions = []
        
        # Har detected face ke liye
        for (x, y, w, h) in faces:
            # Face region extract karo
            face_roi = gray[y:y+h, x:x+w]
            
            # Emotion predict karo
            emotion, confidence = self.predict_emotion(face_roi)
            
            # Store detected emotion
            detected_emotions.append({
                'emotion': emotion,
                'confidence': confidence,
                'bbox': (x, y, w, h)
            })
            
            # Frame pe rectangle draw karo (green color)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            
            # Emotion label aur confidence display karo
            label = f"{emotion} ({confidence*100:.1f}%)"
            
            # Background rectangle for better text visibility
            label_size, _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)
            cv2.rectangle(
                frame,
                (x, y - 30),
                (x + label_size[0], y),
                (0, 255, 0),
                cv2.FILLED
            )
            
            # Text draw karo
            cv2.putText(
                frame,
                label,
                (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 0, 0),
                2
            )
        
        return frame, detected_emotions

# ============================================
# Standalone Testing Function
# ============================================
def test_webcam():
    """
    Webcam se live emotion detection test karta hai
    Press 'q' to quit
    """
    print("=" * 50)
    print("🎭 MoodSense AI - Webcam Test")
    print("=" * 50)
    
    try:
        # Emotion detector initialize karo
        detector = EmotionDetector()
        
        # Webcam open karo (0 = default webcam)
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            print("❌ ERROR: Could not open webcam!")
            print("\n🔧 Troubleshooting:")
            print("1. Check if webcam is connected")
            print("2. Check if any other app is using webcam")
            print("3. Try running as administrator")
            return
        
        print("✅ Webcam opened successfully!")
        print("👉 Press 'q' to quit")
        
        while True:
            # Frame capture karo
            ret, frame = cap.read()
            
            if not ret:
                print("❌ Failed to grab frame")
                break
            
            # Frame process karo
            processed_frame, emotions = detector.process_frame(frame)
            
            # Show frame
            cv2.imshow('MoodSense AI - Emotion Detection', processed_frame)
            
            # Console mein emotion print karo
            if emotions:
                for emo in emotions:
                    print(f"Detected: {emo['emotion']} (Confidence: {emo['confidence']*100:.1f}%)")
            
            # 'q' press karke exit karo
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        # Cleanup
        cap.release()
        cv2.destroyAllWindows()
        print("👋 Webcam closed!")
        
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()

# ============================================
# MAIN EXECUTION
# ============================================
if __name__ == "__main__":
    # Standalone test ke liye
    test_webcam()
