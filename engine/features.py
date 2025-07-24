from playsound import playsound
import eel
import time
import re
import os
import pywhatkit as kit
import webbrowser
import sqlite3
import pyaudio
import pvporcupine
import struct
import pyautogui

from engine.config import ASSISTANT_NAME
from engine.command import *
from engine.helper import extract_yt_term

# Initialize SQLite connection and cursor
conn = sqlite3.connect('jarvis.db')  
cursor = conn.cursor()

@eel.expose #helps to acces the function from JavaScript
def playAssitantSound():
    time.sleep(1)
    music_dir = r"www/assets/vendore/texllate/audio/www_assets_audio_start_sound.mp3"
    playsound(music_dir)

def openCommand(query):
    

    query = query.replace(ASSISTANT_NAME.lower(), "")
    query = query.replace("open", "")
    query = query.lower()

    app_name = query.strip()  # remove leading and trailing spaces

    if app_name != "":

        try:  # to handle errors
            cursor.execute(
                'SELECT path FROM sys_command WHERE name IN (?)', (app_name,))
            results = cursor.fetchall()# returns a list of tuples

            if len(results) != 0:
                speak("Opening " + query)
                os.startfile(results[0][0])

            elif len(results) == 0:
                cursor.execute(
                    'SELECT url FROM web_command WHERE name IN (?)', (app_name,))
                results = cursor.fetchall()

                if len(results) != 0:
                    speak("Opening " + query)
                    webbrowser.open(results[0][0])

                else:
                    speak("Opening " + query)
                    try:
                        os.system('start ' + query)
                    except Exception:
                        speak("not found")
        except Exception:
            speak("something went wrong")


def PlayYoutube(query):
    search_term = extract_yt_term(query)
    if search_term:
        speak("playing " + search_term + " on youtube")
        kit.playonyt(search_term)
    else:
        speak("Sorry, I could not extract the search term from your command.")


def hotword():
    print("Hotword detection started...")
    porcupine=None
    paud=None
    audio_stream=None
    try:
        # pre trained keywords    
        porcupine = pvporcupine.create(keywords=["jarvis", "alexa"])
        paud = pyaudio.PyAudio()
        audio_stream = paud.open(rate=porcupine.sample_rate, channels=1, format=pyaudio.paInt16, input=True, frames_per_buffer=porcupine.frame_length)

        # loop for streaming
        while True:
            keyword = audio_stream.read(porcupine.frame_length, exception_on_overflow=False)
            keyword = struct.unpack_from("h" * porcupine.frame_length, keyword)

            # processing keyword comes from mic 
            keyword_index = porcupine.process(keyword)

            # checking first keyword detected or not
            if keyword_index >= 0:
                print("hotword detected")

                # pressing shortcut key win+j
                pyautogui.keyDown("win")
                pyautogui.press("j")
                time.sleep(2)
                pyautogui.keyUp("win")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        if porcupine is not None:
            porcupine.delete()
        if audio_stream is not None:
            audio_stream.close()
        if paud is not None:
            paud.terminate()



