import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hidden_recipes.settings')

import re
regex = re.compile(r"\n\s*", re.MULTILINE)

import django
django.setup()
from django.contrib.auth.models import User
from website.models import Tag, UserProfile, Recipe, Comment
from django.utils import timezone

def populate():
    cuisine_tags = ["African", "American", "British", "Caribbean",
        "Chinese", "East European", "French", "Greek", 
        "Indian", "Irish", "Italian", "Japanese", 
        "Korean", "Mexican", "Nordic", "North African", 
        "Pakistani", "Portugese", "South American", 
        "Spanish", "South-East Asian", "Middle Eastern"]
    
    ingredient_tags = ["Artichoke", "Asparagus", "Beef", "Beetroot", "Bread", 
                       "Broccoli", "Brussels Sprouts", "Butter", "Cabbage", "Carrot", "Celery", 
                       "Cheese", "Chicken", "Coconut Milk", "Cream", "Cucumber", "Eggs", "Garlic", 
                       "Green Beans", "Herbs", "Honey", "Kale", "Lamb", "Leek", "Lemon", "Lentils", "Lettuce", 
                       "Lime", "Milk", "Mozzarella", "Mushrooms", "Mustard", "Noodles", "Nuts", 
                       "Olive Oil", "Onion", "Parmesan", "Parsnip", "Pasta", "Peppers", "Pork", 
                       "Potato", "Rice", "Soy Sauce", "Spices", "Spinach", "Sweet Potato", 
                       "Tomato", "Turnip", "Yoghurt"]

    print("Adding Cuisine Tags")
    for tag in cuisine_tags:
        add_tag(tag)

    print("Adding Ingredient Tags")
    for tag in ingredient_tags:
        add_tag(tag)

    users = [{
            "username": "foodlover99",
            "bio": "#1 recipe enjoyer in the Principality of Sealand. Stay-at-home mum 🏠💪",
            "picture": "bean1.png"
        },
        {
            "username": "toorteebteai",
            "bio": "Food Purist and personal trainer. I post only the highest-quality healthy recipes!",
            "picture": "evilbean.png"
        }]

    print("Adding Users")
    for user in users:
        add_user(user)

    recipes = [{
            "username": "toorteebteai",
            "title": "Home-style Chicken Curry",
            "description": "This authentic recipe traces its roots back to my father's upbringing in a Bihari household in Northern India. A relatively mild dish (with options to increase the spice level), enjoy it with rice or even naan and some vegetable curry.",
            "ingredients": """5-6 cloves
                5-6 cardamoms broken into small pieces
                Under 10cm cinnamon broken into small pieces
                1 large onion
                1 red chilli (optional)
                5 garlic cloves
                4-5 medium tomatoes
                500g chicken (I use thighs and drumsticks)
                Coriander powder / some mixed spice powder
                2 spoons yoghurt
                1 bunch of coriander""",
            "instructions": """Chop your onion decently small (at least 1 square cm). If you want it, cut the red chilli into pieces (to reduce potential spiciness, cut down the side and remove the seeds from the inside). Chop the garlic quite fine. Chop the tomatoes into quarters."
                Put about 2 tablespoons of oil in a large pan and heat it. Add the whole spices and fry for a few minutes. Then add the onions and chilli and fry for a few minutes. Then add the garlic and fry for a few more minutes.
                Add your pieces of chicken and mix them with the other stuff. Add a spoon of some spice powder and salt. Mix well and fry for 10 minutes.
                Add two spoons of yoghurt and the tomatoes. Cover the pan with a lid, turn the heat down and cook for 20 minutes.
                Chop a bunch of coriander after cutting off the base. After the 20 minutes, add the coriander, stir and cook for 10 more minutes.""",
            "tags": ["Indian", "Chicken", "Garlic", "Onion", "Tomato", "Yoghurt", "Spices"],
            "picture": "chickencurry.png"
        },
        {
            "username": "foodlover99",
            "title": "Quick chicken fajitas",
            "description": "Fajitas are one of my favourite dishes, and with this quick recipe you can easily whip up a batch for a weeknight dinner. Don't forget to grab your favourite toppings!",
            "ingredients": """500g chicken thighs
            2 peppers, ideally of different colours
            1 medium onion / red onion
            A packet of fajita seasoning
            To serve: about 10 tortillas
            Your favourite additions e.g. salsa, guacamole, cheese, sour cream""",
            "instructions": """Cut the peppers and onion into long, thin strips. Fun fact - the word \"fajita\" means \"little strip\", referring to the strips you're cutting now.
            Cut your chicken into similar sized strips (maybe a bit wider than the veggies).
            Head 1 tbsp of oil in a large frying pan - ideally a griddle pan but any frying pan will do. 
            Fry your veggies for a minute or two on high heat. This step is crucial in ensuring the correct texture of the veggies!
            Take the veggies out of the pan. Add the chicken and fry on slightly lower heat until it's well browned.
            Sprinkle over your fajita seasoning, stir and fry for a few minutes.
            Add your veggies back to the pan, stir well and fry for a minute or two more.
            Serve in tortilla wraps with your choice of toppings!""",
            "tags": ["Mexican", "American", "Chicken", "Onion", "Peppers"],
            "picture": "fajitas.png"
        },
        {
            "username": "toorteebteai",
            "title": "Cashew nut chicken",
            "description": "This Chinese-inspired dish requires a few ingredients you may not already have - but its delicious flavour makes acquiring them well worth it! I recommend serving it with noodles.",
            "ingredients": """=== For the sauce ===
            4 tablespoons soy sauce
            5 tablespoons rice wine vinegar
            1 tablespoon sesame oil
            3 tablespoons chopped root ginger
            2 tablespoons honey
            60ml chicken or vegetable stock
            1 tablespoon cornflour (essential)
            1 tablespoon chilli oil (not required)
            1 teaspoon chilli garlic paste (not required)
            === For the chicken ===
            2 tablespoons vegetable oil (1 tablespoon sunflower, 1 tablespoon sesame oil)
            500g chicken breast chunks
            1 onion, chopped
            1 green pepper, chopped
            1 tin water chestnuts, drained and sliced (substitute with 1 extra pepper)
            100g cashew nut pieces""",
            "instructions": """Make the sauce by mixing all your sauce ingredients together in a bowl.
            Chop your peppers and chicken into square chunks (relatively large).   
            Heat the oil in a large saucepan over high heat. Stir in the chicken; cook and stir until the chicken is no longer pink, about 5 minutes. Remove the chicken and set aside.
            Stir in the onion, cashews and water chestnuts. Cook and stir until the cashew nuts are browned, chestnuts are hot, and the onion has softened - about 5 minutes more. Throw in the pepper near the end of this.
            Add back the chicken, turn down the heat, put on the lid, and cook for 5 minutes.
            Increase the heat again. Stir up the sauce to redistribute the cornflour, then pour into the wok. Stir until the sauce thickens.""",
            "tags": ["Chinese", "Chicken", "Peppers", "Onion", "Soy Sauce", "Nuts"],
            "picture": "cashewchicken.png"
        },
        {
            "username": "foodlover99",
            "title": "Simple Tacos",
            "description": "As a tex-mex cuisine connoisseur, I love tacos! They're incredibly simple to make and infinitely customisable.",
            "ingredients": """500g beef mince (substitute for another meat's mince)
            A packet of taco seasoning
            Around 12 taco shells
            To top: I like lettuce, sour cream and jalapeños""",
            "instructions": """Brown your mince in a pan over medium heat. Drain away any excess fat if possible.
            Sprinkle over your taco seasoning and add around 100ml of water. Stir well and simmer until the sauce reduces.
            You can even heat up your taco shells in the microwave! Put them open-end-down on a plate and microwave for 60 seconds.
            Load up your taco shells with taco meat and some delicious toppings. Enjoy!""",
            "tags": ["Mexican", "American", "Beef", "Lettuce"],
            "picture": "tacos.png"
        },
        {
            "username": "toorteebteai",
            "title": "Chilli Paneer",
            "description": "This delicious Indian recipe is a perfect cheat-day snack. Have it as a side along with healthier, more substantial mains - potentially hakka noodles or fried rice due to this dish's Indo-Chinese origins.",
            "ingredients": """=== For the sauce ===
            1 tablespoon soya sauce
            4 tablespoons Maggi Hot and Sweet ketchup
            1/2 teaspoon vinegar
            1/2 teaspoon red chilli powder
            1 teaspoon sugar
            === For the paneer ===
            200-250g paneer, cubed
            3 cloves of garlic, finely chopped
            Half a bunch of spring onions, chopped
            1 pepper, chopped into fairly large square pieces
            1 medium onion, chopped into similar sized pieces and layers separated
            1 chilli, slit and deseeded, chopped into small pieces
            === For the corn slurry ===
            1/4 teaspoon black pepper
            1 teaspoon cornstarch
            1/2 cup water
            """,
            "instructions": """On a medium flame, heat 3 to 4 tablespoons of oil in a deep frying pan.
            Add your paneer and leave it to stand for a bit. Later stir and fry them on a medium heat until all sides are crispy. Remove the paneer from the pan and put on a paper towel to drain.
            Mix together your sauce ingredients to make the sauce. In a small bowl, mix together your corn slurry ingredients.
            Add the garlic to the pan and fry for a couple minutes until it smells good. Then add your pepper, onion, spring onions and chilli and fry for a couple more minutes.
            Add the sauce and the corn slurry into the pan. Stir and fry on a medium heat till the sauce begins to thicken.
            Add the paneer back to the pan and mix well. Fry for a few minutes more.""",
            "tags": ["Indian", "Cheese", "Garlic", "Onion", "Peppers", "Soy Sauce"],
            "picture": "paneer.png"
        },
        ]

    print("Adding Recipes")
    for recipe in recipes:
        add_recipe(recipe)
    
    comments = [{"recipe": "Quick chicken fajitas",
                "username": "toorteebteai",
                "text": "Not a fan of this recipe. It cost me £15 to cook and the chicken didn't taste of anything! There are no dodges to marinating the chicken for fajitas, which is the only correct way to do it. Kids these days... always looking for shortcuts."}]
    
    print("Adding Comments")
    for comment in comments:
        add_comment(comment)

def add_tag(name):
    tag = Tag.objects.get_or_create(name=name)[0]
    tag.save()

def add_recipe(recipe_info):
    newIngredients = regex.sub("\n", recipe_info["ingredients"])
    newInstructions = regex.sub("\n", recipe_info["instructions"])

    recipe = Recipe.objects.get_or_create(title=recipe_info["title"], 
                                          poster=User.objects.get(username=recipe_info["username"]), 
                                          description = recipe_info["description"],
                                          ingredients = newIngredients,
                                          instructions = newInstructions, 
                                          picture = "populate_assets/" + recipe_info["picture"],
                                          date = timezone.now())[0]
    recipe.save()

    for tag in recipe_info["tags"]:
        recipe.tags.add(Tag.objects.get(name=tag))

def add_comment(comment_info):
    comment = Comment.objects.get_or_create(poster=User.objects.get(username=comment_info["username"]), recipe=Recipe.objects.get(title=comment_info["recipe"]), text=comment_info["text"])[0]
    comment.save()

def add_user(user):
    user_obj = User.objects.get_or_create(username=user["username"])[0]
    user_obj.set_password("test")
    user_obj.save()

    profile = UserProfile.objects.get_or_create(user=user_obj)[0]
    profile.bio = user["bio"]
    profile.picture = "populate_assets/" + user["picture"]
    profile.save()


if __name__ == "__main__":
    print("Populating Hidden Recipes")
    populate()