

class IngredientRepository:
    def __init__(self, vector_store, llm):
        self.vector_store = vector_store