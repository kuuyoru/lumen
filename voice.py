from gtts import gTTS
from playsound import playsound
import threading
import uuid
import os
import time

def speak(text, wait=False):
    filename = f"voice_{uuid.uuid4().hex}.mp3"
    filepath = os.path.abspath(filename)

    tts = gTTS(text=text, lang='en')
    tts.save(filepath)
    
    time.sleep(0.2)  # ensure file is fully written before playing

    # Estimate duration: roughly 150 words per minute = 2.5 words per second
    # Add some buffer for processing
    estimated_duration = max(len(text.split()) / 2.5, 1.0) + 0.5

    def play_and_cleanup(path):
        playsound(path)
        time.sleep(0.5)  # wait for file to be released
        try:
            os.remove(path)  # delete after playing
        except PermissionError:
            pass  # file may still be locked, that's ok

    thread = threading.Thread(target=play_and_cleanup, args=(filepath,), daemon=True)
    thread.start()
    
    if wait:
        time.sleep(estimated_duration)  # wait for estimated audio duration