from bs4 import BeautifulSoup 
from requests import get 
from csv import reader, writer 
import json 

all_recipes = []
url = 'https://cooking.nytimes.com/68861692-nyt-cooking/21636-icy-cold-desserts-from-mark-bittman-and-more'
response = get(url)
soup = BeautifulSoup(response.text, "html.parser")

initial_recipes = soup.find_all(attrs={"itemprop": "itemListElement"})
for recipe in initial_recipes:
    recipe_object = {}
    ingredient_list = []
    instruction_list = []
    recipe_url = "https://cooking.nytimes.com" + recipe.a["href"]
    recipe_soup = BeautifulSoup(get(recipe_url).text, "html.parser")
    
    for title in recipe.find_all(attrs={"class": "name"}):
        recipe_object["title"] = title.text.strip()
    for author in recipe.find_all(attrs={"class": "card-byline"}):
        recipe_object["author"] = author.text.strip()
    
       # print(recipe_object)
    ingredients = recipe_soup.find_all(attrs={"itemprop": "recipeIngredient"})
    for ingredient in ingredients:
        ingredient_list.append(ingredient.find("span", attrs={"class": "quantity"}).text.strip() + " " + ingredient.find("span", attrs={"class": "ingredient-name"}).text.strip())
        recipe_object["ingredients"] = ingredient_list
        
    #yield_time = recipe_soup.find_all(attrs={"class": "recipe-yield-value"})
    for result_list in recipe_soup.find_all(attrs={"class": "recipe-yield-value"}):
        if len(result_list) > 1:
            recipe_object["yield_time"] = result_list[1].text
        else:
            recipe_object["yield_time"] = result_list.text

    
    
    recipe_instructions = recipe_soup.find_all(attrs={"itemprop": "recipeInstructions"})
    for instruction in recipe_instructions:
        for instruction_step in instruction.find_all("li"):
            instruction_list.append(instruction_step.text)
            recipe_object["instructions"] = instruction_list
    all_recipes.append(recipe_object)


def recipe_finder(dish):
    for recipe in all_recipes:
        print(recipe["title"])
        if recipe["title"].lower() == dish.lower():
            return(recipe)
        else:
            pass
            
            
def make_plural(word):
    vowels = "aieou"
    alt_endings = ["s", "x", "z", "f", "o", "ch", "sh", "fe"]
    lastLetter = word[len(word)-1]
    lastTwoLetters = word[len(word) -2] + word[len(word)-1]
    
    print(lastLetter)
    print(lastTwoLetters)
    
    if lastLetter in alt_endings and alt_endings.index(lastLetter) < 2:
        return word + "es"
    elif lastLetter in alt_endings and alt_endings.index(lastLetter) == 3:
        return word.replace("f", "ves")
    elif (lastLetter in alt_endings and alt_endings.index(lastLetter) == 4) and not (word[len(word)-2] in vowels):
        return word + "es"
    elif lastLetter == "y" and not (word[len(word)-2] in vowels):
        return word.replace("y", "ies")
    else:
        return word + "s"
        
 def ingredient_search(ingredients):
    results = []
    exclude_list = ["and", "but", "cups", "diced", "or"]
    ingredients = ingredients.split(" ")
    
    print(ingredients)

    
    for recipe in all_recipes:
        for ingredient in ingredients:
            ingredients_in_recipe = " ".join(recipe["ingredients"]).split(" ")
            ingredients_in_recipe = ([x.strip(",") for x in ingredients_in_recipe])
            if ingredient in ingredients_in_recipe and ingredient not in exclude_list:
                results.append(recipe)
            else:
                pass 
    return(results)
    
    
    

recipe_categories = ["chocolate", "ice creams and sorbets", "frozen fruit ice treats"]



            
def launch_intent():
    launch_question = questions["launch_question"]
    
    latest_question["question"] = launch_question
    last_statement = ""
    print("here launched!!")
    
    return(question(launch_question))

def ingredient_intent(dish):
    recipe = recipe_finder(dish)
    print(recipe)
    if type(recipe) == type(dict()):
        print("yay!")
        statements["neededIngredientStatement"] = "To make {0} you will need the following:   ".format(dish) + "   ".join(recipe["ingredients"]).replace("/", " or ")
        return(statement(statements["neededIngredientStatement"]))
    else: 
        print("welp!")
        statements["IngredientsUnknownStatement"] =  "Sorry, I'm not sure what the ingredients for {0} are".format(str(dish))
        return(statement(statements["IngredientsUnknownStatement"]))


def no_intent():
    print("the no intent was called")  
    
    if latest_question["question"] == questions["launch_question"]:
        exitConfirmation1 = questions["exitConfirmation1"]
        latest_question["question"] = exitConfirmation1
        return(question(exitConfirmation1))
    if latest_question["question"] == questions["exitConfirmation1"]:
        recipeInMind = questions["recipeInMind"]
        latest_question["question"] = questions["recipeInMind"]
        return(question(recipeInMind))
    if latest_question["question"] == questions["recipeInMind"]:
        recipeCategories = questions["recipeCategories"]
        latest_question["question"] = questions["recipeCategories"]
        return(question(recipeCategories))
        
    else:
        return(statement("bye!!"))

def yes_intent():
    print("the yes intent was called")
    if latest_question["question"] == questions["launch_question"]:
        recipeInMind = questions["recipeInMind"]
        latest_question["question"] = recipeInMind
        return(question(recipeInMind))
    if latest_question["question"] == questions["exitConfirmation1"]:
        return(statement("Okay, enjoy the heat."))
    if latest_question["question"] == questions["recipeInMind"]:
        nameRecipe = questions["nameRecipe"]
        latest_question["question"] = nameRecipe
        return(question(nameRecipe))
        
    else:
        print("done.")
        
# SPEND MORE TIME ON MORE OPTIONS AND REPEAT OPTIONS
def more_options():
    print("more options intent")
    print(latest_question["question"])
    print(latest_category["category"])
    
    if latest_question["question"] == questions["recipeCategories"] and latest_category["category"] == recipe_categories[0]:
        chocolateOptions1 = questions["chocolateOptions1"]
        latest_question["question"] = chocolateOptions1
        return(question(chocolateOptions1))
    elif latest_question["question"] == questions["recipeCategories"] and latest_category["category"] == recipe_categories[1]:
        iceCreamOptions1 = questions["iceCreamOptions1"]
        latest_question["question"] = iceCreamOptions1
        return(question(iceCreamOptions1))
    elif latest_question["question"] == questions["recipeCategories"] and latest_category["category"] == recipe_categories[2]:
        frozenFruitOptions1 = questions["frozenFruitOptions1"]
        latest_question["question"] = frozenFruitOptions1
        return(question(frozenFruitOptions1))
    
#SPEND MORE TIME ON MORE OPTIONS AND REPEAT OPTIONS    
def repeat_options():
    print("more options intent")
    print(latest_question["question"])
    print(latest_category["category"])
    
    if latest_question["question"] == questions["chocolateOptions1"]:
        chocolateOptions1 = questions["chocolateOptions1"]
        latest_question["question"] = chocolateOptions1
        return(question(chocolateOptions1))
    elif latest_question["question"] == questions["iceCreamOptions1"] and latest_category["category"] == recipe_categories[1]:
        iceCreamOptions1 = questions["iceCreamOptions1"]
        latest_question["question"] = iceCreamOptions1
        return(question(iceCreamOptions1))
    elif latest_question["question"] == questions["frozenFruitOptions1"] and latest_category["category"] == recipe_categories[2]:
        frozenFruitOptions1 = questions["frozenFruitOptions1"]
        latest_question["question"] = frozenFruitOptions1
        return(question(frozenFruitOptions1))
    
        
        
        
        

        
        
def title_intent(recipe_title):
    print("title intent was called!!")
    print(recipe_title)
    return(statement("MOVE TO " + recipe_title + " RECIPE FLOW"))
    
def select_category_intent(category):
    print("select category was called.")
    print(category)
    if recipe_categories[0].lower() == category:
        latest_category["category"] = recipe_categories[0]
        return(question(questions["selectChocolateRecipe"]))
    elif recipe_categories[1].lower() == category:
        latest_category["category"] = recipe_categories[1]
        return(question(questions["selectIceCreamRecipe"]))
    elif recipe_categories[2].lower() == category:
        latest_category["category"] = recipe_categories[2]
        return(question(questions["selectFruitTreats"]))
    else:
        print("oops!")
        


## This is how we'll handle the 'state' of our bot 
questions = {
             "launch_question": "Hi! Welcome to your summer Recipe Box, a collection of Icy Cold Desserts to help you beat the heat. Ready to get started?",
             "exitConfirmation1": "Are you sure? We have over a dozen delicious recipes to choose from.",
             "recipeInMind": "Great, do you know what you want to make yet?",
             "nameRecipe": "Great, tell me what you want to make.",
             "recipeCategories": "We've got Chocolate recipes, Ice Creams and Sorbets, and Frozen Fruit Ice Treats. What sounds the yummiest to you?",
             "selectChocolateRecipe": "Do you want to make Frozen Fudge Pops,,,, or Frozen Maple Mouse Pie,,with chocolate mapple sauce. Or would you like to hear more options?",
             "selectIceCreamRecipe": "Do you want to make mango lime sobert or coconut maccaroon and mango bombe? Or would you like to hear more options?",
             "selectFruitTreats": "Do you want to make pineapple, ginger, and cilantro ice pops,,, or tangerine ice? Or would you like to hear more options?",
             "chocolateOptions1": "Okay. Do you want to make Marcella Hazo's Semifreddo di Cioccolato,,, or Frozen Chocolate Souffle? Or would you like to hear your options again?",
             "iceCreamOptions1": "Okay. Do you want to make frozen Espresso Zabagliones; Malted Milk Ice Cream Bonbons; or Cherry Coconut Ice Cream Sandwhiches? Or would would like to hear your options again?",
             "frozenFruitOptions1": "Okay. Do you want to make Frozen Watermelon Slush or Shaved Blueberry Cinnamon Ice? Or do you want to hear more options?"
}

statements = {"neededIngredientStatement": "",
              "ingredientsUnknownStatement": ""
}

latest_question = {
    "question": ""
}

latest_category = {
    "category": ""
}

# we need to update our config and start our bot again
config = [
    ['launch', launch_intent],
    ['AMAZON.NoIntent', no_intent],
    ['AMAZON.YesIntent', yes_intent],
    ['IngredientIntent', ingredient_intent],
    ['getTitleIntent', title_intent],
    ['selectCategoryIntent', select_category_intent],
    ['moreOptionsIntent', more_options],
    ['repeatOptionsIntent', repeat_options]
    
    
]



# create out bot object
bot = AlexaBot(config)

# start up our bot
bot.start()
        
