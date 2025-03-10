import faiss
import numpy as np

from .ingredient_vocab import IngredientVocabulary


class FaissDrinkManager:
    def __init__(self, vocab: IngredientVocabulary):
        self.vocab = vocab
        self.faiss_index = faiss.IndexFlatL2(vocab.get_vector_size())

    def batch_insert(self, drinks):
        self.vocab.update_vocab(drinks)
        vectors = [
            self.vocab.encode_ingredient_vector(drink["ingredients"])
            for drink in drinks
        ]
        self.faiss_index.add(np.array(vectors, dtype=np.float32))

        return self.faiss_index.ntotal - len(drinks)

    def search_drink(self, query_ingredients, k=3):
        query_vector = self.vocab.encode_ingredient_vector(query_ingredients)
        distances, indices = self.faiss_index.search(
            np.array([query_vector], dtype=np.float32), k
        )

        return indices[0]
