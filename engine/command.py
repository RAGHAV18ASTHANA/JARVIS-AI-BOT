import pyttsx3
import speech_recognition as sr
import eel
import time
import os
import pyautogui



@eel.expose  # helps to access the function from JavaScript
def speak(text):
    text=str(text)  # Ensure text is a string
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    engine.setProperty('volume',170)  # Set volume to 170%
    engine.setProperty('rate', 200)  # Set speech rate to 200 words
    
    # Try to display in UI, but continue if UI is not available
    try:
        eel.DisplayMessage(text)  # Display the message in the UI
    except:
        print(f"UI not available, speaking: {text}")
    
    engine.say(text)
    
    # Try to send to UI, but continue if UI is not available
    try:
        eel.receiverText(text)  # Send the text to the UI
    except:
        pass
    
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
def allCommands(message=1):#giving default value to message
    if message==1:
        query = takecommand()
        print(query)
        if query:  # Only send to UI if query is not empty
            eel.senderText(query)  # Send the query to the UI
    else:
        query = message
        if query:  # Only send to UI if query is not empty
            eel.senderText(query)

    # Check if query is empty and return early
    if not query or query.strip() == "":
        time.sleep(1)
        eel.showHood()
        return

    try:
        # Use the query that was already determined above
        print(query)

        if "open" in query:
            from engine.features import openCommand
            openCommand(query)

        if any(phrase in query for phrase in ["introduce yourself", "who are you", "introduce", "hi", "hello"]):
            from engine.features import introduceYourself
            introduceYourself()

        if "open whatsapp" in query or "whatsapp" in query:
            pyautogui.hotkey('win')
            time.sleep(1)
            pyautogui.write('whatsapp')
            time.sleep(1)
            pyautogui.press('enter')
            speak("Opening whatsapp")
            time.sleep(1)
            speak("what you want to do on whatsapp"
                  " send message, phone call or video call")
            query = takecommand()
            if "send message" in query:
                speak("whom to send message")
                query = takecommand()
                from engine.features import findContact, whatsApp
                contact_no, name = findContact(query)
                if(contact_no != 0):
                    speak("what message to send")
                    message = takecommand()
                    whatsApp(contact_no, message, 'message', name)
            elif "phone call" in query or "call" in query:
                speak("whom to call")
                query = takecommand()
                from engine.features import findContact, whatsApp
                contact_no, name = findContact(query)
                if(contact_no != 0):
                    whatsApp(contact_no, query, 'call', name)
            elif "video call" in query:
                speak("whom to video call")
                query = takecommand()
                from engine.features import findContact, whatsApp
                contact_no, name = findContact(query)
                if(contact_no != 0):
                    whatsApp(contact_no, query, 'video call', name)

        elif "turn on wifi" in query or "on wifi" in query or "turn off wifi" in query or "off wifi" in query or "turn on bluetooth" in query or "on bluetooth" in query or "turn off bluetooth" in query or "off bluetooth" in query:
            from engine.features import pccommands
            pccommands(query)  # Call the pccommands function with the query    

        elif "on youtube" in query:
            from engine.features import PlayYoutube
            PlayYoutube(query)

        elif "send message" in query  or "message" in query or "phone call" in query or "call" in query or "video call" in query:
            from engine.features import findContact, whatsApp
            contact_no, name = findContact(query)
            if(contact_no != 0):
                if "send message" in query or "message" in query:
                    message_flag = 'message'
                    speak("what message to send")
                    message_content = takecommand()
                    whatsApp(contact_no, message_content, message_flag, name)

                elif "video call" in query:  # Check video call BEFORE phone call
                    message_flag = 'video call'
                    whatsApp(contact_no, query, message_flag, name)
                    
                elif "phone call" in query or "call" in query:
                    message_flag = 'call'
                    whatsApp(contact_no, query, message_flag, name)

        else:
            from engine.features import chatBot
            chatBot(query)  # Call the chatbot function with the query

        # Always return to the starting page after command execution
        time.sleep(1)  # Wait for a second before showing the hood
        eel.showHood()  # Show the hood after command execution

    except Exception as e:
        print("An error occurred while processing the command:", e)
        time.sleep(1)  # Wait for a second before showing the hood
        eel.showHood()  # Show the hood after recognitions 

