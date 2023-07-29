import dotenv

from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain, SimpleSequentialChain
from langchain.output_parsers import StructuredOutputParser
from modules.roles_templates.roles_templates import roles_templates
from modules.schemas.brain_schema import response_schemas
from modules.langchain_assistant.utils import create_prompt_template, check_format

dotenv.load_dotenv()
llm = ChatOpenAI(temperature=0.5)

output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
format_instructions = output_parser.get_format_instructions()

class LangChainProductivityAssistant:
    def __create_chain(self, prompt_template):
        return LLMChain(llm=llm, prompt=prompt_template)

    def __create_prompts_template(self):
        return [
            create_prompt_template(role_template, format_instructions)
            for role_template in roles_templates
        ]

    def __create_chains(self, prompts_template):
        return [
            self.__create_chain(prompt_template)
            for prompt_template in prompts_template
        ]

    def chat(self, input):
        prompts_template = self.__create_prompts_template()
        chains = self.__create_chains(prompts_template)
        overall_chain = SimpleSequentialChain(
            chains=chains,
            verbose=True
        )
        response = check_format(overall_chain.run(input))
        return output_parser.parse(response)
