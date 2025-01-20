import speech_recognition as sr

def recognize_speech():
    mic_index = 6  # Example index, replace with the correct one
    sr.Microphone.list_microphone_names()
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone(device_index=mic_index) as source:
            print("Speak the spell: ")
            audio = recognizer.listen(source)

        try:
            spell = recognizer.recognize_google(audio)
            print(f"You said: {spell}")
            return spell
        except sr.UnknownValueError:
            print("Sorry, I could not understand the audio.")
            return None
        except sr.RequestError:
            print("Could not request results from Google Speech Recognition service.")
            return None
    except OSError:
        print("Microphone not found. Please type the spell.")
        return input("Type the spell: ")