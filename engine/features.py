from playsound import playsound
import eel
import time

@eel.expose #helps to acces the function from JavaScript
def playAssitantSound():
    time.sleep(2)
    music_dir="www\\assets\\vendore\\texllate\\audio\\www_assets_audio_start_sound.mp3"
    playsound(music_dir)
