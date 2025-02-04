# 2. Similarity Search with Relevance Scores

```
[
  (
    Document(id='f696b88a-6b96-4256-9dfb-783db1e3829f', metadata={'source': './app/storage/recipes.csv', 'row': 10}, page_content='drink_name: Strawberry Lemonade\ndrink_category: Lemonade\nflavors: Strawberry,Lemonade Non-Sweetened,Water,Cane Sugar\nflavor_volumes: Strawberry:22,Lemonade Non-Sweetened:31,Water:286,Cane Sugar:16'),
    0.2274848502598199
  ),
  (
    Document(id='a0e5c005-d0f4-4d8f-8ee1-d145db73d715', metadata={'source': './app/storage/recipes.csv', 'row': 11}, page_content='drink_name: Strawberry Lemonade Smoothie\ndrink_category: Smoothie\nflavors: Strawberry,Lemonade Non-Sweetened,Cane Sugar,Water\nflavor_volumes: Strawberry:31,Lemonade Non-Sweetened:34,Cane Sugar:30,Water:82'),
    0.2016788406787816
  ),
  (
    Document(id='99145679-0521-4b26-8efc-bd74931ed0f1', metadata={'source': './app/storage/recipes.csv', 'row': 4}, page_content='drink_name: Mango Passion Fruit Smoothie\ndrink_category: Smoothie\nflavors: Mango,Lemonade Non-Sweetened,Passion Fruit,Cane Sugar,Water\nflavor_volumes: Mango:34,Lemonade Non-Sweetened:12,Passion Fruit:22,Cane Sugar:14,Water:95'),
    0.020229745756227047
  )
]
```

# 3. Similarity Search with Score

```
[
  (
    Document(id='a2a053a9-8472-42ef-a253-5eab2f361bc2', metadata={'source': './app/storage/recipes.csv', 'row': 10}, page_content='drink_name: Strawberry Lemonade\ndrink_category: Lemonade\nflavors: Strawberry,Lemonade Non-Sweetened,Water,Cane Sugar\nflavor_volumes: Strawberry:22,Lemonade Non-Sweetened:31,Water:286,Cane Sugar:16'),
    1.0920336
  ),
  (
    Document(id='7ca8ebc0-9a59-4a12-8219-a5a475730e7d', metadata={'source': './app/storage/recipes.csv', 'row': 11}, page_content='drink_name: Strawberry Lemonade Smoothie\ndrink_category: Smoothie\nflavors: Strawberry,Lemonade Non-Sweetened,Cane Sugar,Water\nflavor_volumes: Strawberry:31,Lemonade Non-Sweetened:34,Cane Sugar:30,Water:82'),
    1.1291511
  ),
  (
    Document(id='a6c76c80-1de2-4ad5-b25d-14afb185095f', metadata={'source': './app/storage/recipes.csv', 'row': 4}, page_content='drink_name: Mango Passion Fruit Smoothie\ndrink_category: Smoothie\nflavors: Mango,Lemonade Non-Sweetened,Passion Fruit,Cane Sugar,Water\nflavor_volumes: Mango:34,Lemonade Non-Sweetened:12,Passion Fruit:22,Cane Sugar:14,Water:95'),
    1.3843633
  )
]
```
