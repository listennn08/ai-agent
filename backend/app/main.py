import json
from typing import List
import faiss
from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from langchain_core.messages import HumanMessage, AIMessage, trim_messages
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import CSVLoader
from pydantic import BaseModel, Field


# Load environment variables from .env file
load_dotenv()

# Initialize FastAPI
app = FastAPI()

# Initialize OpenAI embeddings
embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
llm = ChatOpenAI(model="gpt-4o")

# Load Recipes from CSV
recipes = CSVLoader("recipes.csv").load_and_split()

# Initialize FAISS
index = faiss.IndexFlatL2(len(embeddings.embed_query(" ")))
vector_store = FAISS(
    embedding_function=embeddings,
    index=index,
    docstore=InMemoryDocstore(),
    index_to_docstore_id={},
)

# Add Recipes to Vector Store
vector_store.add_documents(recipes)

# Create a retriever from the vector store
retriever = vector_store.as_retriever()

# record the history of interactions
history = []


class DrinkRecipe(BaseModel):
    name: str = Field(description="The name of the drink")
    ingredients: List[str] = Field(description="The ingredients of the drink")

class DrinkRecipes(BaseModel):
    recipes: List[DrinkRecipe] = Field(description="The recipes of the drink")

@app.get("/retrieve")
def retrieve_drink(user_input: str):
    try:
        # Retrieve relevant recipes
        recipes = vector_store.similarity_search(user_input)

        template = """
        Based on these recipes: {recipes}
        and the user's preference: {user_input},
        get the name and ingredients of the drink.
        If no drink is found, return an empty list.

        {format_instructions}
        """

        parser = PydanticOutputParser(pydantic_object=DrinkRecipes)
        prompt = PromptTemplate(
            template=template,
            input_variables=["user_input"],
            partial_variables={
                "recipes": recipes,
                "format_instructions": parser.get_format_instructions()
            }
        )

        chain = prompt | llm | parser

        response = chain.invoke({ "user_input": user_input })

        return response
    except Exception as e:
        return str(e)

# API: Generate New Drink
@app.post("/generate")
def generate_drink(user_input: str):
    try:
        selected_history = trim_messages(
            messages=history,
            token_counter=len,
            max_tokens=5,
            strategy="last",
            start_on="human",
            include_system=True,
            allow_partial=False,
        )

        # If has generated recipes, include in prompt
        recipes = vector_store.similarity_search(user_input, k=3)
        print(selected_history)
        # Generate new drink idea
        template = """
        Here is the history of the conversation: {history}
        ---
        Based on these recipes: {recipes}
        and the user's preference: {user_input},
        create a new and unique drink recipe that considers the flavor percentages.
        If user input want to adjust the previous recipes, do not create another drink
        and don't rename the previous recipes unless specified by the user.

        {format_instructions}
        """

        parser = PydanticOutputParser(pydantic_object=DrinkRecipe)
        prompt = PromptTemplate(
            template=template,
            input_variables=["user_input", "history"],
            partial_variables={
                "recipes": recipes,
                "history": selected_history,
                "format_instructions": parser.get_format_instructions()
            }
        )

        chain = prompt | llm | parser

        response = chain.invoke({ "user_input": user_input })

        history.append(HumanMessage(user_input))
        history.append(AIMessage(json.dumps(response.json())))

        return response
    except Exception as e:
        # print detail and line
        print(e)
        raise HTTPException(status_code=500, detail=str(e))