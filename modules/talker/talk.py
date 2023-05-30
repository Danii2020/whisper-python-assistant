import pyttsx3
import fakeyou
import tempfile
import os
import time
from pygame import mixer

fake_you = fakeyou.FakeYou()

class FakeYouTalker:
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
        self.__login_to_fakeyou()
        temp_file = tempfile.mkdtemp()
        filename = os.path.join(temp_file, 'temp.wav')
        tts_model_token = self.__get_tts_token(self.model_name)
        print(tts_model_token)
        fake_you.say(text=text, ttsModelToken=tts_model_token, filename=filename)
        return filename

    def talk(self, text):
        mixer.init()
        filename = self.__generate_audio(text)
        mixer.music.load(filename)
        audio_duration = mixer.Sound(filename).get_length()
        mixer.music.play()
        time.sleep(audio_duration)


class TtsTalker:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 145)
        self.voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', self.voices[3].id)

    def talk(self, text):
        self.engine.say(text)
        self.engine.runAndWait()


class Talker:
    def __init__(self, talker_cls):
        self.talker_cls = talker_cls

    def talk(self, text):
        self.talker_cls.talk(text)

