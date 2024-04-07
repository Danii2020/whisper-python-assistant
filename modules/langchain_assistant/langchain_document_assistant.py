import dotenv
from langchain_openai import ChatOpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA

dotenv.load_dotenv()
llm = ChatOpenAI(temperature=0.2)

class LangChainDocumentAssistant:
    def __init__(self, document_name) -> None:
        self.document_name = document_name
        raw_document = PyPDFLoader(f'{self.document_name}').load()
        character_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        document = character_splitter.split_documents(raw_document)

        database = FAISS.from_documents(documents=document, embedding=OpenAIEmbeddings())
        self.qa = RetrievalQA.from_chain_type(llm=llm, retriever=database.as_retriever())

    def chat(self, query):
        result = self.qa.run(query)
        return result
