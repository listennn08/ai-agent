# Initialize OpenAI embeddings
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

load_dotenv()


embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

def get_llm(model: str = "gpt-4o"):
    return ChatOpenAI(model=model)