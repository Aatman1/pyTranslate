import speech_recognition as sr
import noisereduce as nr
import numpy as np

def listen_speech(audio_queue):
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Adjusting for ambient noise... Please wait.")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        recognizer.energy_threshold = 300
        recognizer.dynamic_energy_threshold = True
        print("Listening...")

        while True:
            try:
                print("Waiting for voice...")
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
                print("Voice detected, processing...")

                # Convert audio to numpy array
                audio_data = np.frombuffer(audio.get_raw_data(), dtype=np.int16)

                # Apply noise reduction
                reduced_noise = nr.reduce_noise(y=audio_data, sr=source.SAMPLE_RATE, n_fft=2048, hop_length=512)

                # Convert the noise-reduced numpy array back to audio data
                audio_data = sr.AudioData(reduced_noise.tobytes(), source.SAMPLE_RATE, audio.sample_width)

                # Perform speech recognition
                text = recognizer.recognize_google(audio_data)
                print(f"You said: {text}")
                audio_queue.put(text)
            except sr.WaitTimeoutError:
                continue  # Just continue waiting for voice input
            except sr.UnknownValueError:
                print("")
            except sr.RequestError as e:
                print(f"Could not request results from Google Speech Recognition service; {e}")
            except Exception as e:
                print(f"Listening error: {e}")
