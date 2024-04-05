import tempfile
import os
import pygame
import time
from gtts import gTTS


def play_message(message: str):
    lang = "en"
    tts = gTTS(text=message, lang=lang)

    with tempfile.TemporaryDirectory() as tmp_dir:
        print(tmp_dir)
        tmp_file_path = os.path.join(tmp_dir, "temp.mp3")
        tts.save(tmp_file_path)

        pygame.mixer.init()
        pygame.mixer.music.load(tmp_file_path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)
        pygame.mixer.quit()
