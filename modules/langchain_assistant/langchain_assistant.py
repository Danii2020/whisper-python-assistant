class LangChainAssistant:
    def __init__(self, langchain_role):
        self.langchain_role = langchain_role

    def chat(self, input):
        return self.langchain_role.chat(input)