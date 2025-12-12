from gtts import gTTS
import pygame
import io

word  = "fuck you"

# Create TTS audio
tts = gTTS(word, lang="ja")
mp3_data = io.BytesIO()
tts.write_to_fp(mp3_data)

# Reset pointer
mp3_data.seek(0)

# Initialize pygame mixer
pygame.mixer.init()

# Load and play
pygame.mixer.music.load(mp3_data)
pygame.mixer.music.play()

# Keep script alive until done playing
while pygame.mixer.music.get_busy():
    pass
