import dotenv

from langchain.chat_models import ChatOpenAI
# from langchain.prompts.chat import (
#     ChatPromptTemplate,
#     SystemMessagePromptTemplate,
#     HumanMessagePromptTemplate,
# )
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SimpleSequentialChain
from langchain.agents import load_tools, initialize_agent, AgentType
from langchain.output_parsers import StructuredOutputParser
from modules.roles_templates.roles_templates import roles_templates
from modules.schemas.brain_schema import response_schemas
import langchain

dotenv.load_dotenv()
llm = ChatOpenAI(temperature=0.2)
tools = load_tools(["google-serper"], llm=llm)
output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
format_instructions = output_parser.get_format_instructions()
print(format_instructions)
# langchain.debug = True

class LangChainBrainAssistant:
    def __create_chain(self):
        prompt_template = roles_templates.get("prompt_template")
        prompt = PromptTemplate(
            template=prompt_template,
            input_variables=["output"],
            partial_variables={"format_instructions": format_instructions}
        )
        return LLMChain(llm=llm, prompt=prompt)

    def __create_agent(self):
        return initialize_agent(
            tools=tools,
            llm=llm,
            agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION,
            handle_parsing=True,
            verbose=False
        )

    def chat(self, input):
        agent = self.__create_agent()
        chain = self.__create_chain()
        overall_chain = SimpleSequentialChain(
            chains=[agent, chain],
            verbose=False
        )
        response = overall_chain.run(input)
        print(response)
        return output_parser.parse(response)
