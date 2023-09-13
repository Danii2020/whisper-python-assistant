from modules.talker.talk import Talker, TtsTalker
from modules.listen import Listener
from modules.notion.notion_integration import Notion
from modules.langchain_assistant.langchain_assistant import LangChainAssistant
from modules.langchain_assistant.langchain_productivy_assistant import LangChainProductivityAssistant
from modules.langchain_assistant.langchain_browser_assistant import LangChainBrowserAssistant
from modules.langchain_assistant.langchain_scientist_assistant import LangChainScientisAssistant
from modules.langchain_assistant.langchain_chat_assistant import LangChainChatAssistant

talker = Talker(TtsTalker())
listener = Listener()
notion = Notion()

langchain_roles = {
    "productivo": LangChainProductivityAssistant,
    "navegador": LangChainBrowserAssistant,
    "científico": LangChainScientisAssistant,
    "chat": LangChainChatAssistant,
}

def say_welcome(role):
    talker.talk(
        f"Hola, bienvenido al modo {role},"
        " hazme cualquier pregunta que necesites"
    )

def listen_to_response():
    return input("Escribe tu pregunta: ")

def generate_reponse(role, user_prompt):
    langchain_role = langchain_roles[role]()
    response = LangChainAssistant(langchain_role).chat(user_prompt)
    return response

def create_notion_page(data):
    properties = {
        "Name": {"title": [{"text": {"content": f"{data.get('title', None)}"}}]},
        }
    children_page = [{"object": "block", "paragraph":{"rich_text":[{"text":{"content":f"{data.get('content', None)}"}}]}}]
    notion.create_page(properties=properties, children=children_page)

def identify_role(user_prompt):
    if "cambia a modo" in user_prompt:
        user_prompt = user_prompt.rstrip(".")
        words = user_prompt.split()
        roles = ["productivo", "navegador", "científico", "chat"]
        matched_roles = [word for word in words if word in roles]
        if len(matched_roles) >= 1:
            return matched_roles[0]
        else:
            talker.talk("No conozco ese modo!")
            return None

def display_and_store_response(response):
    content = response.get('content', None)
    try:
        print(content)
        talker.talk(content)
        create_notion_page(response)
    except:
        print(response)
        talker.talk(response)

def handle_user_input(role, user_prompt):
    possible_role = identify_role(user_prompt=user_prompt)
    if possible_role:
        if possible_role == role:
            talker.talk("Ya estás en ese rol!")
        else:
            start_role(possible_role)
    assistant_response = generate_response(role=role, user_prompt=user_prompt)
    display_and_store_response(assistant_response)


def start_role(role):
    say_welcome(role)
    while True:
        user_prompt = listen_to_response()
        if "termina" in user_prompt:
            break
        handle_user_input(role, user_prompt)
