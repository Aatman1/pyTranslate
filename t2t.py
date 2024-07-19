from transformers import MarianMTModel, MarianTokenizer
import torch

def translate_text(audio_queue, text_queue, target_language):
    src_lang = 'en'  # assuming source language is English
    tgt_lang = target_language

    model_name = f'Helsinki-NLP/opus-mt-{src_lang}-{tgt_lang}'
    tokenizer = MarianTokenizer.from_pretrained(model_name)
    model = MarianMTModel.from_pretrained(model_name).to('cuda' if torch.cuda.is_available() else 'cpu')

    while True:
        if not audio_queue.empty():
            text = audio_queue.get()
            print(f"You said: {text}")

            model_inputs = tokenizer(text, return_tensors="pt").to('cuda' if torch.cuda.is_available() else 'cpu')
            translated = model.generate(**model_inputs)
            translated_text = tokenizer.decode(translated[0], skip_special_tokens=True)
            combined_text = f"You said: {text}\nTranslated: {translated_text}"
            text_queue.put(combined_text)
