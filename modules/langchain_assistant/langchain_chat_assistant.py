import dotenv
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from modules.roles_templates.roles_templates import roles_templates
from langchain.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder
)

from langchain.memory import (
    ConversationBufferMemory,
    ConversationBufferWindowMemory,
    ConversationEntityMemory
)

dotenv.load_dotenv()
llm = ChatOpenAI(temperature=0.5)

class LangChainChatAssistant:
    def __init__(self) -> None:
        assistant_prompt = SystemMessagePromptTemplate.from_template(
            template=roles_templates[0].get("prompt_template")
        )
        user_prompt = HumanMessagePromptTemplate.from_template("{input}")
        message_placeholder = MessagesPlaceholder(variable_name="chat_history")
        chat_prompt = ChatPromptTemplate.from_messages(
            [assistant_prompt, message_placeholder, user_prompt]
        )
        self.response = LLMChain(
            llm=llm,
            prompt=chat_prompt,
            verbose=True,
            memory=ConversationEntityMemory(chat_history_key="chat_history", return_messages=True, llm=llm)
        )

    def chat(self, input):
        print("MEMORY:\n")
        print(self.response.memory)
        print("ENTITIES:\n")
        print(self.response.memory.entity_store.store)

        return self.response.predict(input=input)
