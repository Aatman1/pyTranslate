import multiprocessing as mp
import time
from s2t import listen_speech
from t2t import translate_text

def main():
    print("Available languages (use ISO 639-1 codes):")
    print("Examples: 'es' for Spanish, 'fr' for French, 'hi' for Hindi")
    target_language = input("Enter the target language code: ").strip()

    audio_queue = mp.Queue()
    text_queue = mp.Queue()
    
    # Create processes for speech recognition and translation
    speech_process = mp.Process(target=listen_speech, args=(audio_queue,))
    translation_process = mp.Process(target=translate_text, args=(audio_queue, text_queue, target_language))

    speech_process.start()
    translation_process.start()

    try:
        while True:
            if not text_queue.empty():
                translated_text = text_queue.get()
                print(f"Translated: {translated_text}")
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("Exiting...")
        speech_process.terminate()
        translation_process.terminate()
        speech_process.join()
        translation_process.join()

if __name__ == "__main__":
    main()
