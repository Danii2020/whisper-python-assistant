from modules.talker.talk import Talker, TtsTalker
from modules.listen import Listener
from modules.notion.notion_integration import Notion
from modules.langchain_assistant.langchain_brain import LangChainBrainAssistant

talker = Talker(TtsTalker())
listener = Listener()
langchain_assistant = LangChainBrainAssistant()
notion = Notion()

def say_welcome():
    talker.talk(
        "Hola, bienvenido al modo sábelo todo,"
        " hazme cualquier pregunta que necesites"
    )

def listen_to_response():
    return listener.listen()

def generate_reponse():
    response = langchain_assistant.chat(listen_to_response())
    return eval(response.content)

def create_notion_page(data):
    properties = {
        "Name": {"title": [{"text": {"content": f"{data.get('title', None)}"}}]},
        }
    children_page = [{"object": "block", "paragraph":{"rich_text":[{"text":{"content":f"{data.get('content', None)}"}}]}}]
    notion.create_page(properties=properties, children=children_page)

def start_brain_mode():
    say_welcome()
    assistant_response = generate_reponse()
    print(assistant_response.get('content', None))
    talker.talk(assistant_response.get('content', None))
    create_notion_page(assistant_response)