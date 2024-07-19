import speech_recognition as sr

def test_microphone():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Adjusting for ambient noise... Please wait.")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("Microphone is ready, start speaking...")

        while True:
            try:
                print("Listening...")
                audio = recognizer.listen(source)
                print("Processing...")
                text = recognizer.recognize_google(audio)
                print(f"You said: {text}")
            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand audio")
            except sr.RequestError as e:
                print(f"Could not request results from Google Speech Recognition service; {e}")
            except Exception as e:
                print(f"Listening error: {e}")

if __name__ == "__main__":
    test_microphone()
