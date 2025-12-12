from gtts import gTTS
import pygame
import io
import time
import sum_reader #import the module with 'total'

# Start the module that generates total
sum_reader.start()

pygame.mixer.init()

def speak(text):
    tts = gTTS(text, lang="ja")
    mp3_data = io.BytesIO()
    tts.write_to_fp(mp3_data)
    mp3_data.seek(0)

    pygame.mixer.music.load(mp3_data)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pass


print("Speaking totals...\n")

while True:
    if sum_reader.total is not None:
        word = str(sum_reader.total)      # <-- total goes here
        print("Speaking:", word)
        speak(word)
    
    time.sleep(1)   # speak every 1 second
