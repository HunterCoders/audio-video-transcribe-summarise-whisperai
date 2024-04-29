![image](https://github.com/HunterCoders/audio-video-transcribe-summarise-whisperai/assets/157727212/094c9a13-3ce7-46c6-a973-23a5064218d8)#packages to be installed
        1.  pip install git+https://github.com/openai/whisper.git  (Whisper API)
        2. choco install ffmpeg
        3. pip install librosa
        4.  pip install nltk

#In case of failures in nltk package run this as scratch python file (Can be deleted later)
      import nltk
      nltk.download('punkt')
      nltk.download('stopwords')
Some test videos that has been tested. 
(Disclaimer: I own no rights to these videos)
      1. https://www.youtube.com/watch?v=VnTVz39FAVQ
      2. https://www.youtube.com/watch?v=xTzvQkOll2U
      3. https://www.youtube.com/watch?v=jiHz12oOpdI


Requirements
Modules Installed/Required:
•	tkinter
•	whisper 3.0
•	soundfile
•	os
•	librosa
•	ffmpeg
Software Requirements:
•	Python 3.11
•	VRAM of ~1GB to ~10GB depending on the Whisper model used (small model requires 2GB).
Methodology
1.	Input Handling:
Utilize tkinter library for creating a simple GUI for selecting input files.
Incorporate a file dialog box for choosing audio or video files.
2.	Audio/Video Processing:
Use librosa library for handling audio/video files.
Split the video into epochs of 30 seconds each.
Extract the audio from each epoch for transcription.
3.	Transcription:
Integrate OpenAI's Whisper API for transcribing audio.
Concatenate the transcriptions from all epochs into a single text.
Detect the language of the transcribed text.
4.	Summarization:
Implement a summarization algorithm based on the number of sentences provided by the user.
Utilize Natural Language Processing techniques for summarization, using NLTK.
Modules
User Interface (UI):
Provides a graphical interface for file selection and interaction with the system.
Audio/Video Processing:
Handles the loading, chunking, and processing of audio/video files.
Transcription:
Utilizes Whisper API for audio transcription, detecting the language of the content.
Summarization:
Implements summarization algorithm using NLTK based on a user-specified number of sentences.


Views: <br>
1.	File Selection<br>
![image](https://github.com/HunterCoders/audio-video-transcribe-summarise-whisperai/assets/157727212/0d616d12-15e4-4420-a44f-b8e59a44f65c)<br>
2.	Wrong Format Chosen<br>
![image](https://github.com/HunterCoders/audio-video-transcribe-summarise-whisperai/assets/157727212/40fe3ec7-e6ee-468b-bf92-f87575754698)<br>
3.	File broken down into chunks.<br>
![image](https://github.com/HunterCoders/audio-video-transcribe-summarise-whisperai/assets/157727212/ef4180ec-0e6a-43f1-b07d-2f473b264c62)<br>
4.	Transcription started<br>
![image](https://github.com/HunterCoders/audio-video-transcribe-summarise-whisperai/assets/157727212/6ce5112b-caa3-46bd-8c32-420cfc385f72)<br>
5.	Transcription Completed for all chunks<br>
![image](https://github.com/HunterCoders/audio-video-transcribe-summarise-whisperai/assets/157727212/414b940c-d705-4420-93b7-796d9cba8166)<br>
7.	Number of sentences required for summary<br>
![image](https://github.com/HunterCoders/audio-video-transcribe-summarise-whisperai/assets/157727212/d4386c8e-c2b6-485c-aee5-1b279eeda82f)<br>
8.	Summary Generated<br>
![image](https://github.com/HunterCoders/audio-video-transcribe-summarise-whisperai/assets/157727212/f48b2d0b-8bd1-4289-8eb9-804d37de04d3)<br>


      
      
