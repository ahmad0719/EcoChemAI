
from api import analyze

ingredient = input("Ingredient: ")

print("\nThinking...\n")

answer = analyze(ingredient)

print(answer)