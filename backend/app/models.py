from pydantic import BaseModel, Field
from typing import List


class DrinkIngredient(BaseModel):
    name: str = Field(description="The name of the ingredient")
    percentage: float = Field(description="The percentage of the ingredient")
    volume: float = Field(description="The volume of the ingredient")


class DrinkRecipe(BaseModel):
    name: str = Field(description="The name of the drink")
    img: str = Field(description="The image of the drink")
    ingredients: List[DrinkIngredient] = Field(description="The ingredients of the drink")


class MessageResponse(BaseModel):
    message: str = Field(description="The message of the response")
    recipe: DrinkRecipe | None = Field(description="The recipe of the response")

class DrinkRecipes(BaseModel):
    recipes: List[DrinkRecipe] = Field(description="The recipes of the drink")


class UserInput(BaseModel):
    user_input: str = Field(description="The user input")


class BooleanModel(BaseModel):
    bool_value: bool = Field(description="The boolean value")