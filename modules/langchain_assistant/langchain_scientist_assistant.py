import dotenv

from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain, SimpleSequentialChain
from langchain.agents import load_tools, initialize_agent, AgentType
from modules.roles_templates.roles_templates import roles_templates
from modules.langchain_assistant.utils import create_prompt_template

dotenv.load_dotenv()
llm = ChatOpenAI(temperature=0.1)
tools = load_tools(["wolfram-alpha", "wikipedia"], llm=llm)

class LangChainScientisAssistant:
    def __create_translator_chain(self):
        prompt_template = create_prompt_template(roles_templates[-2])
        return LLMChain(llm=llm, prompt=prompt_template)

    def __create_agent(self):
        return initialize_agent(
            tools=tools,
            llm=llm,
            agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION,
            handle_parsing=True,
            verbose=True
        )

    def chat(self, input):
        agent = self.__create_agent()
        chain = self.__create_translator_chain()
        overall_chain = SimpleSequentialChain(
            chains=[agent, chain],
            verbose=True
        )
        response = overall_chain.run(input)
        response = {
            "title": input,
            "content": response
        }
        return response
