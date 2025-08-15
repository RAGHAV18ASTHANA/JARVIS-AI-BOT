from shlex import quote
import subprocess
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
import google.generativeai as genai

from engine.config import ASSISTANT_NAME
from engine.command import *
from engine.helper import *


# Initialize SQLite connection and cursor
conn = sqlite3.connect('jarvis.db')  
cursor = conn.cursor()

@eel.expose #helps to acces the function from JavaScript
def playAssitantSound():
    time.sleep(1)
    music_dir = r"www/assets/vendore/texllate/audio/www_assets_audio_start_sound.mp3"
    playsound(music_dir)
def introduceYourself():
    speak("Hello, I am Jarvis, your personal assistant. I can help you with various tasks like opening applications, sending messages, and more. How can I assist you today?")

@eel.expose  # helps to access the function from JavaScript
def openCommand(query):
    

    query = query.replace(ASSISTANT_NAME.lower(), "")
    query = query.replace("open", "")
    query = query.lower()

    app_name = query.strip()  # remove leading and trailing spaces

    if app_name != "whatsapp":

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
        porcupine = pvporcupine.create(keywords=["alexa", "jarvis"])
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

def findContact(query):

    words_to_remove = [ASSISTANT_NAME, 'make', 'a', 'to', 'phone', 'call', 'send', 'message', 'wahtsapp', 'video','on', 'whatsapp']
    query = remove_words(query, words_to_remove)

    try:
        query = query.strip().lower()
        cursor.execute("SELECT mobile_no FROM contacts WHERE LOWER(name) LIKE ? OR LOWER(name) LIKE ?", ('%' + query + '%', query + '%'))
        results = cursor.fetchall()
        print(results[0][0])
        mobile_number_str = str(results[0][0])

        if not mobile_number_str.startswith('+91'):
            mobile_number_str = '+91' + mobile_number_str

        return mobile_number_str, query
    except:
        speak('not exist in contacts')
        return 0, 0


def whatsApp(mobile_no, message, flag, name):
    if flag == 'message':
        target_tab = 12
        jarvis_message = "Message sent successfully to " + name
        # Encode the message for URL
        encoded_message = quote(message)
        whatsapp_url = f"whatsapp://send?phone={mobile_no}&text={encoded_message}"
    elif flag == 'call':
        target_tab = 7
        message = ''
        jarvis_message = "Calling " + name
        whatsapp_url = f"whatsapp://send?phone={mobile_no}"  # No message for call
    else:  # Assuming this is for video call
        target_tab = 6
        message = ''
        jarvis_message = "Starting video call with " + name
        whatsapp_url = f"whatsapp://send?phone={mobile_no}"  # No message for call
    # Construct the full command
    full_command = f'start "" "{whatsapp_url}"'
    # Open WhatsApp with the constructed URL using cmd.exe
    try:
        subprocess.run(full_command, shell=True)
        time.sleep(5)  # Wait for WhatsApp to open
        # If you want to navigate to a specific tab, you can do so here
        pyautogui.hotkey('ctrl', 'f')
        time.sleep(1)
        for i in range(1, target_tab):
            pyautogui.hotkey('tab')
        time.sleep(1)
        pyautogui.hotkey('enter')
        speak(jarvis_message)
    except Exception as e:
        print(f"An error occurred: {e}")

def pccommands(query):
    query = query.lower()
    
    def check_wifi_status():
        """Check if WiFi is currently enabled"""
        try:
            import subprocess
            result = subprocess.run(['netsh', 'wlan', 'show', 'profiles'], 
                                  capture_output=True, text=True, shell=True)
            return "There is no wireless interface on the system." not in result.stdout
        except:
            return None  # Unable to determine status
    
    def check_bluetooth_status():
        """Check if Bluetooth is currently enabled"""
        try:
            import subprocess
            result = subprocess.run(['powershell', 'Get-PnpDevice', '-Class', 'Bluetooth', '-Status', 'OK'], 
                                  capture_output=True, text=True, shell=True)
            return len(result.stdout.strip()) > 0
        except:
            return None  # Unable to determine status
    
    if "turn on wifi" in query or "on wifi" in query:
        wifi_status = check_wifi_status()
        if wifi_status is True:
            speak("WiFi is already turned on")
        elif wifi_status is False:
            speak("Turning on WiFi")
            pyautogui.hotkey('win', 'a')
            time.sleep(2)
            pyautogui.press('enter')
            time.sleep(1)
            speak("WiFi turned on successfully")
        else:
            speak("Checking WiFi status...")
            pyautogui.hotkey('win', 'a')
            time.sleep(2)
            pyautogui.press('enter')
            time.sleep(1)
            speak("WiFi toggle attempted")
        
    elif "turn off wifi" in query or "off wifi" in query:
        wifi_status = check_wifi_status()
        if wifi_status is False:
            speak("WiFi is already turned off")
        elif wifi_status is True:
            speak("Turning off WiFi")
            pyautogui.hotkey('win', 'a')
            time.sleep(2)
            pyautogui.press('enter')
            time.sleep(1)
            speak("WiFi turned off successfully")
        else:
            speak("Checking WiFi status...")
            pyautogui.hotkey('win', 'a')
            time.sleep(2)
            pyautogui.press('enter')
            time.sleep(1)
            speak("WiFi toggle attempted")
    
    elif "turn on bluetooth" in query or "on bluetooth" in query:
        bluetooth_status = check_bluetooth_status()
        if bluetooth_status is True:
            speak("Bluetooth is already turned on")
        elif bluetooth_status is False:
            speak("Turning on Bluetooth")
            pyautogui.hotkey('win', 'a')
            time.sleep(2)
            pyautogui.press('tab')
            time.sleep(1)
            pyautogui.press('enter')
            time.sleep(1)
            speak("Bluetooth turned on successfully")
        else:
            speak("Checking Bluetooth status...")
            pyautogui.hotkey('win', 'a')
            time.sleep(2)
            pyautogui.press('tab')
            time.sleep(1)
            pyautogui.press('enter')
            time.sleep(1)
            speak("Bluetooth toggle attempted")
        
    elif "turn off bluetooth" in query or "off bluetooth" in query: 
        bluetooth_status = check_bluetooth_status()
        if bluetooth_status is False:
            speak("Bluetooth is already turned off")
        elif bluetooth_status is True:
            speak("Turning off Bluetooth")
            pyautogui.hotkey('win', 'a')
            time.sleep(2)
            pyautogui.press('tab')
            time.sleep(1)
            pyautogui.press('enter')
            time.sleep(1)
            speak("Bluetooth turned off successfully")
        else:
            speak("Checking Bluetooth status...")
            pyautogui.hotkey('win', 'a')
            time.sleep(2)
            pyautogui.press('tab')
            time.sleep(1)
            pyautogui.press('enter')
            time.sleep(1)
            speak("Bluetooth toggle attempted")

    # def create_folder(folder_name):
    #     """Create a folder with the given name"""
    #     try:
    #         # Use an absolute path or specify a base directory if needed
    #         folder_path = os.path.abspath(folder_name)
    #         os.makedirs(folder_path, exist_ok=True)
    #         speak(f"Folder '{folder_path}' created successfully.")
    #     except Exception as e:
    #         speak(f"Error creating folder: {e}")  
    
    # def delete_folder(folder_name):
    #     """Delete a folder with the given name"""
    #     try:
    #         folder_path = os.path.abspath(folder_name)
    #         if os.path.exists(folder_path):
    #             os.rmdir(folder_path)
    #             speak(f"Folder '{folder_path}' deleted successfully.")
    #         else:
    #             speak(f"Folder '{folder_path}' does not exist.")
    #     except Exception as e:
    #         speak(f"Error deleting folder: {e}") 

    # if "create folder" in query:
    #     # Extract folder name from the query
    #     folder_name = query.replace("create folder", "").strip()
    #     if folder_name:
    #         create_folder(folder_name)
    #     else:
    #         speak("Please specify a folder name to create.") 

    # elif "delete folder" in query:
    #     # Extract folder name from the query
    #     folder_name = query.replace("delete folder", "").strip()
    #     if folder_name:
    #         delete_folder(folder_name)
    #     else:
    #         speak("Please specify a folder name to delete.")    

    else:
        speak("Unknown command for PC operations.")


def chatBot(query):
    try:
        API_KEY = "AIzaSyBho0NV69yF8TqyOmfY3ufgBUa_kn3x39U"
        genai.configure(api_key=API_KEY)

        model = genai.GenerativeModel("gemini-2.0-flash")
        chat = model.start_chat()
        
        # Use the query parameter instead of input()
        user_input = query.lower()
        if user_input == "exit":
            print("Exiting the chatbot.")
            return "Goodbye!"

        response = chat.send_message(user_input)
        print(f"Jarvis: {response.text}")
        
        # Use the speak function that's already imported
        speak(response.text)  # Make Jarvis speak the response
        return response.text
        
    except Exception as e:
        print(f"Error in AI chatbot: {e}")
        speak("Sorry, I'm having trouble connecting to my AI service.")
        return "AI service error"


# def chatBot(query):
#     user_input = query.lower()
#     chatbot = hugchat.ChatBot(cookie_path="engine\cookies.json")
#     id = chatbot.new_conversation()
#     chatbot.change_conversation(id)
#     response =  chatbot.chat(user_input)
#     print(response)
#     speak(response)
#     return response

