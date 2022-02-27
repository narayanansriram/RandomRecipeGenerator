import requests
import json

#read in text file
with open('static//microservice//recipe_input.json', 'r') as reciperequirements:
    requirements = json.load(reciperequirements)

#build api call with key:value pairs
response = "https://api.spoonacular.com/recipes/complexSearch?apiKey=3b471402d2804b7ca86b11cbbcbe76cd&number=1"
for i in range(0, len(requirements)):
    key = list(requirements.keys())[i]
    value = list(requirements.values())[i]
    response += "&" + key + "=" + str(value)

responseCall = requests.get(response).json()

#extract just the id
thisRecipeList = list(responseCall.values())[0]
print("thisRecipeList->",thisRecipeList)
thisRecipeDict = thisRecipeList[0]
thisID = list(thisRecipeDict.items())[0][1]

#pull information from APi about the recipe
recipeinfo = requests.get("https://api.spoonacular.com/recipes/" + str(thisID) + "/information?apiKey=3b471402d2804b7ca86b11cbbcbe76cd").json()

#write information to json file
with open('static//microservice//recipe.json', 'w') as recipeFile:
    recipejson = json.dumps(recipeinfo)
    recipeFile.write(recipejson)
recipeFile.close()


print(response)