import os

import gtts
import speech_recognition
import librosa
import soundfile


def synthesize(text, lang, filename):
    """
    Use gtts.gTTS(text=text, lang=lang) to synthesize speech,
    then save it to filename.

    @params:
    text (str) - the text you want to synthesize
    lang (str) - the language in which you want to synthesize it
    filename (str) - the filename in which it should be saved
    """
    if not isinstance(text, str) or not text.strip():
        raise ValueError("text must be a non-empty string")

    if not isinstance(lang, str) or not lang.strip():
        raise ValueError("lang must be a non-empty string")

    if not isinstance(filename, str) or not filename.strip():
        raise ValueError("filename must be a non-empty string")

    speech = gtts.gTTS(text=text, lang=lang)
    speech.save(filename)


def make_a_corpus(texts, languages, filenames):
    """
    Create many speech files and check their content using SpeechRecognition.
    The files are created as MP3, converted to WAV, and then recognized.

    @param:
    texts - list of texts to synthesize
    languages - list of language codes
    filenames - list of root filenames without ".mp3"

    @return:
    recognized_texts - list of recognized strings
    """
    if not (
        len(texts) == len(languages) == len(filenames)
    ):
        raise ValueError(
            "texts, languages, and filenames must have the same length"
        )

    recognizer = speech_recognition.Recognizer()
    recognized_texts = []

    for text, lang, root_filename in zip(texts, languages, filenames):
        mp3_filename = f"{root_filename}.mp3"
        wav_filename = f"{root_filename}.wav"

        try:
            # Step 1: Synthesize and save as MP3
            synthesize(text, lang, mp3_filename)

            # Step 2: Load MP3 and convert to WAV
            audio_data, sample_rate = librosa.load(
                mp3_filename,
                sr=None,
                mono=True
            )

            soundfile.write(
                wav_filename,
                audio_data,
                sample_rate
            )

            # Step 3: Recognize speech from WAV
            with speech_recognition.AudioFile(wav_filename) as source:
                audio = recognizer.record(source)

            recognized_text = recognizer.recognize_google(
                audio,
                language=lang
            )

            recognized_texts.append(recognized_text)

        except speech_recognition.UnknownValueError:
            recognized_texts.append("Speech could not be recognized")

        except speech_recognition.RequestError as error:
            recognized_texts.append(
                f"Recognition service error: {error}"
            )

        except Exception as error:
            recognized_texts.append(f"Error: {error}")

    return recognized_texts


# Example
texts = [
    "Hello, how are you?",
    "こんにちは"
]

languages = [
    "en",
    "ja"
]

filenames = [
    "english_speech",
    "japanese_speech"
]

results = make_a_corpus(texts, languages, filenames)

for original, recognized in zip(texts, results):
    print("Original:", original)
    print("Recognized:", recognized)
    print()