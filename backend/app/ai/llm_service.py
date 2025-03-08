from langchain_openai import ChatOpenAI, OpenAIEmbeddings

from configs.settings import settings


class LLMService:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            print("== Initialize LLMService ==")
            cls._instance = super(LLMService, cls).__new__(cls)

            cls._instance.embeddings = OpenAIEmbeddings(
                api_key=settings.OPENAI_API_KEY,
                model=settings.EMBEDDING_MODEL
            )
        
        return cls._instance

    
    def get_llm(self, model: str = settings.LLM_MODEL, temperature: float = 0.8):
        self.llm = ChatOpenAI(
            api_key=settings.OPENAI_API_KEY,
            model=model,
            temperature=temperature
        )
        return self.llm
    
    def get_embeddings(self):
        return self.embeddings
