import pyttsx3
import fakeyou
import tempfile
import os
import time
from pygame import mixer
from synthetic_voice import syntetize_voice

fake_you = fakeyou.FakeYou()

class Talk:
    def __init__(self, username, password, model_name):
        self.username = username
        self.password = password
        self.model_name = model_name

    def __login_to_fakeyou(self):
        fake_you.login(self.username, self.password)

    def __get_tts_token(self, model_name):
        result = fake_you.search(model_name)
        return result.voices.modelTokens[0]

    def __generate_audio(self, text):
        temp_file = tempfile.mkdtemp()
        filename = os.path.join(temp_file, 'temp.wav')
        synthetic_audio = syntetize_voice(text, filename)
        return synthetic_audio

    def talk(self, text):
        mixer.init()
        filename = self.__generate_audio(text)
        mixer.music.load(filename)
        audio_duration = mixer.Sound(filename).get_length()
        mixer.music.play()
        time.sleep(audio_duration)
