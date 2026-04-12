import asyncio
import edge_tts

AUDIO_FILE = "voice.mp3"

async def main():
    communicate = edge_tts.Communicate("Hello this is a test", "en-US-AriaNeural")
    await communicate.save(AUDIO_FILE)
    print("DONE SAVING")

asyncio.run(main())