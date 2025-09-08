import speech_recognition as sr

class STT:

    def __init__(self):
        self.SR = sr
        self.Recognizer = sr.Recognizer()

    def convert_audio_to_text(self, audio):
        audio_data = self.SR.AudioFile(audio)
        with audio_data as audio_file:
            data = self.Recognizer.record(audio_file)

        text = self.Recognizer.recognize_google(data).lower()
        return text

