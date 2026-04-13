# L.U.M.E.N. AI Assistant

A sophisticated voice-controlled AI assistant with advanced speech recognition and synthesis capabilities.

## 🚀 Features

### Enhanced Voice Recognition
- **Advanced Whisper Model**: Uses the 'small' Whisper model for superior accuracy
- **Adaptive Silence Detection**: Automatically calibrates to ambient noise levels
- **Noise Reduction**: Applies noise gating and audio normalization
- **Real-time Processing**: Processes audio in smaller chunks for better responsiveness
- **Device Optimization**: Automatically detects and uses the best available audio input device

### Smart Audio Processing
- **RMS-based Silence Detection**: More accurate than simple amplitude thresholding
- **Audio Normalization**: Prevents clipping and improves recognition quality
- **Noise Gate**: Reduces background noise interference
- **Timeout Protection**: Prevents infinite listening with 10-second timeout

### Thread-Safe Operations
- **Audio Device Locking**: Prevents concurrent access conflicts
- **Speech Synchronization**: Ensures speech commands don't overlap
- **Error Recovery**: Graceful handling of audio device issues

## 🛠️ Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Run the assistant:
```bash
python main.py
```

## 🧪 Testing

Test the enhanced listening functionality:
```bash
python test_listening.py
```

## 🎯 Usage

The assistant responds to voice commands including:
- **Time queries**: "What time is it?"
- **Web browsing**: "Open YouTube" or "Open Google"
- **System control**: "Exit" or "Shutdown"

## 🔧 Configuration

The system automatically configures itself for optimal performance:
- Detects the best audio input device
- Calibrates silence thresholds based on environment
- Uses optimized Whisper model settings

## 📋 Requirements

- Python 3.8+
- Microphone/audio input device
- Internet connection (for some features)
- Speakers/audio output device

## 🏗️ Architecture

- `main.py`: Main application loop
- `voice.py`: Text-to-speech functionality
- `voice_whisper.py`: Enhanced speech recognition
- `assistant.py`: Command processing logic

## 🔒 Safety Features

- Audio device access synchronization
- Timeout protection against hanging
- Graceful error handling
- Resource cleanup (temporary files)

## 🎙️ Voice Recognition Improvements

The listening system has been significantly enhanced with:

1. **Better Model**: Upgraded from 'base' to 'small' Whisper model
2. **Adaptive Calibration**: Automatically adjusts to room noise
3. **Noise Processing**: Filters out background interference
4. **Improved Timing**: Faster response with smaller processing chunks
5. **Device Intelligence**: Selects optimal audio hardware
6. **Error Resilience**: Continues working despite audio issues