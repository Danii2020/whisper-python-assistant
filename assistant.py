import pyttsx3
import pywhatkit
from modules.listen import Listener
from modules.talk import Talk


def main():
    listener = Listener()
    talker = Talk('daniiee', 'BlAn2919', 'bob esponja')
    try:
        response = listener.listen()
        if 'reproduce' in response:
            song = response.replace('reproduce', '')
            talker.talk(f"Reproduciendo {song}")
            pywhatkit.playonyt(song)
    except Exception as e:
        print(f"Los siento no te entendí debido a este error: {e}")
        print(e)



if __name__ == '__main__':
    main()

