import speech_recognition as sr
from langdetect import detect
from googletrans import Translator
from gtts import gTTS
import io
from IPython.display import Audio, display


def service_transcribe_audio_to_english(file_path: str) -> (str, str):
    """
    Transcribes a .wav audio file, detects language, and translates to English if necessary.
    Returns:
        english_text (str): Transcribed English text
        source_lang (str): Original detected language code
    """
    print("  [Service] Transcribing audio...")
    recognizer = sr.Recognizer()

    try:
        with sr.AudioFile(file_path) as source:
            audio = recognizer.record(source)
        text = recognizer.recognize_google(audio)  # Google handles speech recognition
        source_lang = detect(text)
        print(f"  [Service] Recognized: '{text}' (Lang: {source_lang})")

        if source_lang != "en":
            translator = Translator()
            english_text = translator.translate(text, src=source_lang, dest="en").text
            print(f"  [Service] Translated to English: '{english_text}'")
            return english_text, source_lang
        else:
            return text, "en"

    except Exception as e:
        print(f"  [Service] ERROR during transcription: {e}")
        return None, None


def service_convert_english_to_speech(text: str, target_lang: str) -> io.BytesIO:
    """
    Converts English text into speech.
    If target_lang != English, text is translated to target_lang first.
    Returns:
        fp (io.BytesIO): In-memory mp3 audio file
    """
    print(f"  [Service] Converting English text to speech in '{target_lang}'...")

    final_text = text
    if target_lang != "en":
        try:
            translator = Translator()
            final_text = translator.translate(text, src="en", dest=target_lang).text
            print(f"  [Service] Translated English -> {target_lang}: '{final_text}'")
        except Exception as e:
            print(f"  [Service] ERROR during translation: {e}")
            final_text = text

    try:
        tts = gTTS(text=final_text, lang=target_lang, slow=False)
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        print("  [Service] In-memory audio file created successfully.")

        # Play inside Jupyter/Colab
        display(Audio(fp.read(), autoplay=True))
        return fp
    except Exception as e:
        print(f"  [Service] ERROR during TTS: {e}")
        return None