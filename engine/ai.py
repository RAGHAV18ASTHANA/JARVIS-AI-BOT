# from urllib import response
# import google.generativeai as genai

# from command import speak

# # Configure the Google Generative AI API
# # Make sure to set your API key
# # You can set it as an environment variable or directly in the code               
# def chatbot(query):
    # try:
    #     API_KEY = "AIzaSyBho0NV69yF8TqyOmfY3ufgBUa_kn3x39U"
    #     genai.configure(api_key=API_KEY)

    #     model = genai.GenerativeModel("gemini-2.0-flash")
    #     chat = model.start_chat()
        
    #     # Use the query parameter instead of input()
    #     user_input = query.lower()
    #     if user_input == "exit":
    #         print("Exiting the chatbot.")
    #         return "Goodbye!"

    #     response = chat.send_message(user_input)
    #     print(f"Jarvis: {response.text}")
        
    #     # Import speak function locally to avoid circular imports
    #     from command import speak
    #     speak(response.text)  # Make Jarvis speak the response
    #     return response.text
        
    # except Exception as e:
    #     print(f"Error in AI chatbot: {e}")
    #     # Import speak function locally to avoid circular imports
    #     try:
    #         from command import speak
    #         speak("Sorry, I'm having trouble connecting to my AI service.")
    #     except:
    #         print("Could not speak error message")
    #     return "AI service error"

# This function is called from your main command handler

