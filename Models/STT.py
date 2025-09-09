import speech_recognition as sr

class STT:

    def __init__(self):
        self.SR = sr # holds the library
        self.Recognizer = sr.Recognizer() # holds the recognizer who send the audio to service

    # gets audio file and convert it to text
    def convert_audio_to_text(self, audio):
        audio_data = self.SR.AudioFile(audio)
        with audio_data as audio_file:
            data = self.Recognizer.record(audio_file)

        text = self.Recognizer.recognize_google(data).lower() # use the Google service to convert to txet
        return text

