from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any


class CreateDrinkIngredient(BaseModel):
    flavor: str = Field(description="flavor sku")
    name: str = Field(description="ingredient name")
    ratio: float = Field(description="ingredient ratio")
    sugar_level: int = Field(description="sugar level")
    volume_ml: float = Field(description="ingredient volume by ml")
    ingredient_ratio: float = Field(description="ingredient ratio")


class CreateDrink(BaseModel):
    sku: str = Field(description="The sku of drink")
    name: str = Field(description="The name of the drink")
    ingredients: List[CreateDrinkIngredient] = Field(
        description="The ingredients of the drink"
    )
    default_volume: float = Field(description="Drink default volume by ml")
    description: str = Field(description="Drink description")
    drink_category: str = Field(description="Drink category")


class DrinkIngredient(BaseModel):
    name: str = Field(description="The name of the ingredient")
    percentage: float = Field(description="The percentage of the ingredient")
    volume: float = Field(description="The volume of the ingredient")


class DrinkRecipe(BaseModel):
    sku: str = Field(description="The sku of the drink")
    name: str = Field(description="The name of the drink")
    ingredients: List[DrinkIngredient] = Field(
        description="The ingredients of the drink"
    )
    relevant_score: float = Field(description="The relevant score of the drink")


class KeywordMessage(BaseModel):
    message: str = Field(description="The message of the response")
    keywords: List[str] = Field(description="The keywords of the response")
    anti_keywords: List[str] = Field(description="The anti-keywords of the response")


class MessageResponse(BaseModel):
    message: str = Field(description="The message of the response")
    drinks: List[DrinkRecipe] = Field(description="The drinks of the response")


class DrinkRecipes(BaseModel):
    recipes: List[DrinkRecipe] = Field(description="The recipes of the drink")


class UserInput(BaseModel):
    user_input: str = Field(description="The user input")


class UserPreferenceBase(BaseModel):
    preferences: Dict[str, Any] = Field(
        default_factory=dict, description="User preferences as key-value pairs"
    )


class UserPreference(UserPreferenceBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True


class BooleanModel(BaseModel):
    bool_value: bool = Field(description="The boolean value")


class Response(BaseModel):
    message: str = Field(description="The message of the response")
    drinks: Optional[List[DrinkRecipe]] = Field(
        description="The drinks of the response"
    )
