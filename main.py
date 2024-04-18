import tkinter as tk
from tkinter import filedialog
import os
import librosa
import soundfile as sf
import whisper
from tkinter import simpledialog
from tkinter import messagebox

import summarizer

LANGUAGES = {
    "en": "english",
    "zh": "chinese",
    "de": "german",
    "es": "spanish",
    "ru": "russian",
    "ko": "korean",
    "fr": "french",
    "ja": "japanese",
    "pt": "portuguese",
    "tr": "turkish",
    "pl": "polish",
    "ca": "catalan",
    "nl": "dutch",
    "ar": "arabic",
    "sv": "swedish",
    "it": "italian",
    "id": "indonesian",
    "hi": "hindi",
    "fi": "finnish",
    "vi": "vietnamese",
    "he": "hebrew",
    "uk": "ukrainian",
    "el": "greek",
    "ms": "malay",
    "cs": "czech",
    "ro": "romanian",
    "da": "danish",
    "hu": "hungarian",
    "ta": "tamil",
    "no": "norwegian",
    "th": "thai",
    "ur": "urdu",
    "hr": "croatian",
    "bg": "bulgarian",
    "lt": "lithuanian",
    "la": "latin",
    "mi": "maori",
    "ml": "malayalam",
    "cy": "welsh",
    "sk": "slovak",
    "te": "telugu",
    "fa": "persian",
    "lv": "latvian",
    "bn": "bengali",
    "sr": "serbian",
    "az": "azerbaijani",
    "sl": "slovenian",
    "kn": "kannada",
    "et": "estonian",
    "mk": "macedonian",
    "br": "breton",
    "eu": "basque",
    "is": "icelandic",
    "hy": "armenian",
    "ne": "nepali",
    "mn": "mongolian",
    "bs": "bosnian",
    "kk": "kazakh",
    "sq": "albanian",
    "sw": "swahili",
    "gl": "galician",
    "mr": "marathi",
    "pa": "punjabi",
    "si": "sinhala",
    "km": "khmer",
    "sn": "shona",
    "yo": "yoruba",
    "so": "somali",
    "af": "afrikaans",
    "oc": "occitan",
    "ka": "georgian",
    "be": "belarusian",
    "tg": "tajik",
    "sd": "sindhi",
    "gu": "gujarati",
    "am": "amharic",
    "yi": "yiddish",
    "lo": "lao",
    "uz": "uzbek",
    "fo": "faroese",
    "ht": "haitian creole",
    "ps": "pashto",
    "tk": "turkmen",
    "nn": "nynorsk",
    "mt": "maltese",
    "sa": "sanskrit",
    "lb": "luxembourgish",
    "my": "myanmar",
    "bo": "tibetan",
    "tl": "tagalog",
    "mg": "malagasy",
    "as": "assamese",
    "tt": "tatar",
    "haw": "hawaiian",
    "ln": "lingala",
    "ha": "hausa",
    "ba": "bashkir",
    "jw": "javanese",
    "su": "sundanese",
    "yue": "cantonese",
}


# Function to handle file selection
# The following module uses filedialog modules that uses a pop up window to accept files
def choose_file():
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    file_path = filedialog.askopenfilename()  # Open file dialog

    # Check if a file is selected
    if not file_path:
        return None

    # Check if the file has a valid extension
    valid_extensions = ['.mp3', '.mp4', '.mpeg', '.mpga', '.m4a', '.wav', '.webm']
    if not any(file_path.lower().endswith(ext) for ext in valid_extensions):
        messagebox.showerror("Error", "Selected file is not a valid audio or video file.")
        return None

    return file_path


# The following module breaks down the input into 30 second slices
def chunk_audio(audio, sample_rate, chunk_duration=30):
    chunk_size = chunk_duration * sample_rate
    num_chunks = len(audio) // chunk_size
    chunks = []
    for i in range(num_chunks):
        chunk_start = i * chunk_size
        chunk_end = (i + 1) * chunk_size
        chunks.append(audio[chunk_start:chunk_end])
    return chunks


# The following model clear the directory of any previous chunks
def clear_directory(directory):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)
        elif os.path.isdir(file_path):
            clear_directory(file_path)
            os.rmdir(file_path)


# Choose audio file
audio_file_path = choose_file()
if not audio_file_path:
    print("No file selected. Exiting...")
    audio_file_path = choose_file()


# load audio
audio, sample_rate = librosa.load(audio_file_path, sr=None, mono=True, res_type='kaiser_fast')

# for time issues the input is trimmed to 90 secs
# Trim audio to 90 seconds
trim_duration = 90
if len(audio) > trim_duration * sample_rate:
    audio = audio[:int(trim_duration * sample_rate)]

# load audio and slice it into chunks
audio_chunks = chunk_audio(audio, sample_rate)

# Create a directory to store chunks
output_dir = "audio_chunks"
clear_directory(output_dir)
os.makedirs(output_dir, exist_ok=True)

# Save trimmed audio
trimmed_audio_path = os.path.join(output_dir, "trimmed_audio.wav")  # 90 seconds file
sf.write(trimmed_audio_path, audio, int(sample_rate))

# Load Whisper model
model = whisper.load_model("small")
transcribe = []  # stores the transcription of each chunk

# the chunks are stored as wav files
for i, chunk in enumerate(audio_chunks):
    chunk_path = os.path.join(output_dir, f"chunk_{i}.wav")
    sf.write(chunk_path, chunk, int(sample_rate))

directory = output_dir
language = ""
# all the chunks are read from the directory
for i, filename in enumerate(os.listdir(directory)):
    if filename.endswith(".wav"):  # Check if file is a WAV audio file
        audio_path = os.path.join(directory, filename)
        print(f"Processing file: {audio_path}")

        # Process each chunk
        audio = whisper.load_audio(audio_path)
        chunk = whisper.pad_or_trim(audio)

        # Transcribe the chunk
        mel = whisper.log_mel_spectrogram(chunk).to(model.device)
        _, probs = model.detect_language(mel)
        language = max(probs, key=probs.get)

        # Print detected language
        print(f"Detected language for chunk {i}: {LANGUAGES[language]}")

        # Decode the audio
        options = whisper.DecodingOptions()
        result = whisper.decode(model, mel, options)

        # Print the recognized text
        print(f"Transcription for chunk {i}: {result.text}")
        transcribe.append(result.text)
        print(
            "------------------------------------------------------------------------------------------------------------")

print("All chunks processed.")
print("=====================================***************************************=================================================")

transcription_full = "\n".join(transcribe)
print(transcription_full)

num = simpledialog.askinteger("Number of Sentences", "Enter number of sentences:")
print("=====================================***************************************=================================================")
summary = summarizer.summarize_text(transcription_full, language, num)
print(f"Summary of the transcription is {summary}")
