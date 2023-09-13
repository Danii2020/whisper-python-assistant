import dotenv

from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain, SimpleSequentialChain
from langchain.output_parsers import StructuredOutputParser
from modules.roles_templates.roles_templates import roles_templates
from modules.schemas.brain_schema import response_schemas
from modules.langchain_assistant.utils import create_prompt_template, check_format

from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

dotenv.load_dotenv()
llm = ChatOpenAI(temperature=0.5)

output_parser = StructuredOutputParser.from_response_schemas(response_schemas)

class LangChainChatAssistant:
    def chat(self, input):
        assistant_prompt = SystemMessagePromptTemplate.from_template(roles_templates[0].get("prompt_template"))
        user_prompt = HumanMessagePromptTemplate.from_template("{input}")
        chat_prompt = ChatPromptTemplate.from_messages(
            [assistant_prompt, user_prompt]
        )
        response = chat(chat_prompt.format_prompt(input=input).to_messages())
        return response
