"""
MoodSense AI - System Verification Script
=========================================
Ye script saare components check karega ki sab kuch properly setup hai
"""

import sys
import os

def print_header(text):
    """Print formatted header"""
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60)

def check_python_version():
    """Python version check"""
    print("\n🐍 Checking Python version...")
    version = sys.version_info
    print(f"   Python {version.major}.{version.minor}.{version.micro}")
    
    if version.major >= 3 and version.minor >= 8:
        print("   ✅ Python version is compatible!")
        return True
    else:
        print("   ❌ Python 3.8+ required!")
        return False

def check_packages():
    """Required packages check"""
    print("\n📦 Checking required packages...")
    
    packages = {
        'cv2': 'opencv-python',
        'tensorflow': 'tensorflow',
        'streamlit': 'streamlit',
        'numpy': 'numpy',
        'pandas': 'pandas',
        'sklearn': 'scikit-learn',
        'matplotlib': 'matplotlib',
        'PIL': 'Pillow'
    }
    
    all_installed = True
    
    for module, package in packages.items():
        try:
            __import__(module)
            print(f"   ✅ {package}")
        except ImportError:
            print(f"   ❌ {package} NOT INSTALLED")
            all_installed = False
    
    return all_installed

def check_webcam():
    """Webcam availability check"""
    print("\n📷 Checking webcam...")
    
    try:
        import cv2
        cap = cv2.VideoCapture(0)
        
        if cap.isOpened():
            ret, frame = cap.read()
            cap.release()
            
            if ret:
                print("   ✅ Webcam working!")
                print(f"   Frame size: {frame.shape}")
                return True
            else:
                print("   ⚠️  Webcam detected but cannot read frames")
                return False
        else:
            print("   ❌ Cannot open webcam!")
            print("   Troubleshooting:")
            print("      - Check if webcam is connected")
            print("      - Close other apps using webcam")
            print("      - Check camera permissions")
            return False
            
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
        return False

def check_project_structure():
    """Project files and folders check"""
    print("\n📁 Checking project structure...")
    
    required_files = [
        'app.py',
        'emotion_detector.py',
        'train_model.py',
        'requirements.txt',
        'README.md'
    ]
    
    required_dirs = [
        'data',
        'models'
    ]
    
    all_good = True
    
    # Check files
    for file in required_files:
        if os.path.exists(file):
            print(f"   ✅ {file}")
        else:
            print(f"   ❌ {file} MISSING")
            all_good = False
    
    # Check directories
    for directory in required_dirs:
        if os.path.exists(directory):
            print(f"   ✅ {directory}/")
        else:
            print(f"   ⚠️  {directory}/ NOT FOUND (will be created)")
            os.makedirs(directory, exist_ok=True)
    
    return all_good

def check_dataset():
    """FER-2013 dataset check"""
    print("\n📊 Checking dataset...")
    
    if os.path.exists('data/fer2013.csv'):
        size_mb = os.path.getsize('data/fer2013.csv') / (1024 * 1024)
        print(f"   ✅ fer2013.csv found ({size_mb:.1f} MB)")
        return True
    else:
        print("   ❌ fer2013.csv NOT FOUND")
        print("   Download from: https://www.kaggle.com/datasets/msambare/fer2013")
        print("   Place in: data/fer2013.csv")
        return False

def check_model():
    """Trained model check"""
    print("\n🧠 Checking trained model...")
    
    if os.path.exists('models/emotion_model.h5'):
        size_mb = os.path.getsize('models/emotion_model.h5') / (1024 * 1024)
        print(f"   ✅ emotion_model.h5 found ({size_mb:.1f} MB)")
        
        # Try to load model
        try:
            from tensorflow.keras.models import load_model
            model = load_model('models/emotion_model.h5')
            print(f"   ✅ Model loads successfully!")
            print(f"   Model input shape: {model.input_shape}")
            print(f"   Model output shape: {model.output_shape}")
            return True
        except Exception as e:
            print(f"   ⚠️  Model file exists but cannot load: {str(e)}")
            return False
    else:
        print("   ❌ emotion_model.h5 NOT FOUND")
        print("   Options:")
        print("      1. Train model: python train_model.py")
        print("      2. Create dummy model: python create_dummy_model.py (for testing)")
        return False

def test_face_detection():
    """Test OpenCV face detection"""
    print("\n👤 Testing face detection...")
    
    try:
        import cv2
        
        # Load face cascade
        cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        face_cascade = cv2.CascadeClassifier(cascade_path)
        
        if face_cascade.empty():
            print("   ❌ Cannot load face detection classifier")
            return False
        
        print("   ✅ Face detection classifier loaded!")
        return True
        
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
        return False

def generate_report(results):
    """Generate final report"""
    print_header("SYSTEM VERIFICATION REPORT")
    
    print("\n📋 Component Status:")
    print("-" * 60)
    
    for component, status in results.items():
        emoji = "✅" if status else "❌"
        status_text = "PASS" if status else "FAIL"
        print(f"   {emoji} {component:<30} {status_text}")
    
    print("-" * 60)
    
    total = len(results)
    passed = sum(results.values())
    percentage = (passed / total) * 100
    
    print(f"\n📊 Overall Score: {passed}/{total} ({percentage:.0f}%)")
    
    if percentage == 100:
        print("\n🎉 All checks passed! You're ready to go!")
        print("\n🚀 Next steps:")
        print("   1. If model not trained: python train_model.py")
        print("   2. Run app: streamlit run app.py")
    elif percentage >= 70:
        print("\n⚠️  Most checks passed, but some issues found.")
        print("   Review failed items above and fix them.")
    else:
        print("\n❌ Multiple issues found. Please fix them before proceeding.")
        print("   Check README.md for detailed troubleshooting.")
    
    print("\n" + "=" * 60)

def main():
    """Main verification function"""
    print_header("MoodSense AI - System Verification")
    print("\nChecking if everything is set up correctly...")
    
    results = {}
    
    # Run all checks
    results['Python Version'] = check_python_version()
    results['Required Packages'] = check_packages()
    results['Project Structure'] = check_project_structure()
    results['Webcam'] = check_webcam()
    results['Face Detection'] = test_face_detection()
    results['Dataset'] = check_dataset()
    results['Trained Model'] = check_model()
    
    # Generate report
    generate_report(results)
    
    print("\n💡 Tips:")
    print("   - Run this script anytime to verify setup")
    print("   - Check README.md for detailed instructions")
    print("   - Review code comments for understanding")
    
    print("\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏹️  Verification cancelled by user")
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        input("\nPress Enter to exit...")
