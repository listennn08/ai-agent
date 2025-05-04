WELCOME_PROMPT = """
## Objective
You are greeting a new customer, or a returning customer.

## Past conversation records
{history}

Generate a warm opening:
"""

EXTRACT_KEYWORDS_PROMPT = """
## Objective
Follow below instructions to extract keywords

## Rules
1. ONLY EXTRACT ABOUT taste/flavor of drink or drink-related descriptions from the **user input**.
2. Only when user answer is positive, short and reply to previous conversation, you can refer to last conversation to extract
3. If no keywords are found, please return an empty list.

## User Input
{user_input}

## Context
{context}

## Output format
{format_instructions}
"""


# Clarification agent prompt
CLARIFICATION_PROMPT = """
## Objective
Customer requests may not be clear. Please ask for more details in a friendly way to ensure you can give the best recommendation.
Please capture the user's requests and summarize them into keywords if the customer has already said 2-3 requirements.

## Customer request
{user_input}

## Keywords
{keywords}

## Anti keywords
{anti_keywords}

Please clarify in bartender style:
---
{format_instructions}
"""


# Recommendation agent prompt
RECOMMENDATION_PROMPT = """
## Objective
You are recommending a drink to a customer.

## Rules
1. If the customer has not specified a drink, please recommend a drink based on the available drinks.
2. If available drinks are not enough, please ask the customer if you can recommend something else.

## Customer request
{user_input}

## Available drinks
{drinks}

Please recommend a drink in bartender style:

{format_instructions}
"""
