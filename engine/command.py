import pyttsx3
import speech_recognition as sr
import eel
import time
import os



@eel.expose  # helps to access the function from JavaScript
def speak(text):
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    engine.setProperty('volume',150)  # Set volume to 150%
    engine.setProperty('rate', 174)  # Set speech rate to 174 words
    eel.DisplayMessage(text)  # Display the message in the UI
    engine.say(text)
    engine.runAndWait()

  
def takecommand():
    r= sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening...")
        eel.DisplayMessage("Listening...")
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source,10,6)#listening,speak time

    try:
        print("Recognizing...")
        eel.DisplayMessage("Recognizing...")
        # Using Google Web Speech API to recognize the audio
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
        eel.DisplayMessage(query)
          # Wait for a second before showing the hood
        
        
    except Exception as e:
        return ""
    return query.lower()

@eel.expose  # helps to access the function from JavaScript
def allCommands():
    try:
        query = takecommand()
        print(query)

        if "open" in query:
            from engine.features import openCommand
            openCommand(query)

        elif "on youtube" in query:
            from engine.features import PlayYoutube
            PlayYoutube(query)
        else:
            print("Command not recognized or not implemented.")
    except:
        print("An error occurred while processing the command.")
        time.sleep(1)  # Wait for a second before showing the hood
        eel.showHood()  # Show the hood after recognitions 