import pyttsx3
import speech_recognition as sr

def speak(text):
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    engine.setProperty('volume',150)  # Set volume to 150%
    engine.setProperty('rate', 174)  # Set speech rate to 174 words
    print(voices)
    engine.say(text)
    engine.runAndWait()


def takecommand():
    r= sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source,10,6)#listening,speak time

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
    except Exception as e:
        return ""
    return query.lower()

text=takecommand()

speak(text)