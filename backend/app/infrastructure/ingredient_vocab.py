from repositories.ingredient_repository import IngredientRepository


class IngredientVocabulary:
    def __init__(self, ingredient_repository: IngredientRepository):
        self.ingredient_vocab = []
        self.ingredient_to_index = {}
        self.ingredient_repository = ingredient_repository

    def update_vocab(self, drinks):
        new_ingredients = set()
        for drink in drinks:
            for ingredient in drink["ingredients"]:
                new_ingredients.add(ingredient["name"])
        
        for ingredient in sorted(new_ingredients):
            if ingredient not in self.ingredient_to_index:
                self.ingredient_to_index[ingredient] = len(self.ingredient_vocab)
                self.ingredient_vocab.append(ingredient)
    

    def get_vector_size(self):
        self.ingredient_vocab = self.ingredient_repository.get_all_ingredients()
        return len(self.ingredient_vocab)
    
    def encode_ingredient_vector(self, ingredients):
        vector = [0] * len(self.ingredient_vocab)
        for ingredient in ingredients:
            name = ingredient["name"]
            if name in self.ingredient_to_index:
                vector[self.ingredient_to_index[name]] = ingredient["volume_ml"]
        return vector


def get_ingredient_vocab():
    return IngredientVocabulary()