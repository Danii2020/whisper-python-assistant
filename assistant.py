from modules.listen import Listener
from modules.keywords.keywords import keywords


def main():
    listener = Listener()
    try:
        user_prompt = listener.listen()
        command = list(filter(lambda x: x in user_prompt, keywords))
        if command:
            keywords[command[0]]()
    except Exception as e:
        print(f"Los siento no te entendí debido a este error: {e}")
        print(e)


if __name__ == '__main__':
    main()

