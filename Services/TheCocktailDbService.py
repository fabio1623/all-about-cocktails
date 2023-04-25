import requests

class TheCocktailDbService:
    def __init__(self):
        self.api_base_url = 'https://www.thecocktaildb.com/api/json/v1/1'

    def enrich_cocktails(self, cocktails):
        return [self.enrich_cocktail(cocktail) for cocktail in cocktails if cocktail.get('name') is not None]
    
    def enrich_cocktail(self, cocktail):
        if cocktail is None:
            print('None cocktail provided..')
            return None
        
        cocktail_name = cocktail.get('name')
        if cocktail_name is None:
            print(f'Cocktail name is None : {cocktail}')
            return None
             
        enriched_cocktail = {
            'name' : cocktail_name,
            'thecocktaildb_id' : None,
            'category' : None,
            'iba' : None,
            'alcoholic' : None,
            'instructions' : None,
            'glass' : None,
            'ingredients' : None,
            'thumb' :  None
        }
        
        fetched_cocktail = self.search_cocktail_by_name(cocktail_name)
        if fetched_cocktail is None:
            enriched_cocktail = self.enrich_from_provided_cocktail(enriched_cocktail, cocktail)
        else:
            enriched_cocktail = self.enrich_from_fetched_cocktail(enriched_cocktail, fetched_cocktail)
        
        return enriched_cocktail

    def search_cocktail_by_name(self, name):
        url = f'{self.api_base_url}/search.php?s={name}'
        response = requests.get(url)
        
        if response.status_code != 200:
            print(f"Failed to fetch details for cocktail '{name}'..")
            return None

        data = response.json()
        drinks = data.get('drinks')
        
        if drinks is None or len(drinks) < 1:
            print(f"No drinks found with name '{name}'..")
            return None
        
        return drinks[0]
    
    def enrich_from_provided_cocktail(self, enriched_cocktail, provided_cocktail):
        enriched_cocktail['ingredients'] = self.extract_ingredients_from_provided_cocktail(provided_cocktail)
        return enriched_cocktail
    
    def enrich_from_fetched_cocktail(self, enriched_cocktail, fetched_cocktail):
        enriched_cocktail['thecocktaildb_id'] = int(fetched_cocktail.get('idDrink')) if fetched_cocktail.get('idDrink') is not None else None
        enriched_cocktail['category'] = fetched_cocktail.get('strCategory')
        enriched_cocktail['iba'] = fetched_cocktail.get('strIBA')
        enriched_cocktail['alcoholic'] = fetched_cocktail.get('strAlcoholic')
        enriched_cocktail['glass'] = fetched_cocktail.get('strGlass')
        enriched_cocktail['thumb'] = fetched_cocktail.get('strDrinkThumb')
        enriched_cocktail['instructions'] = self.extract_instructions_from_fetched_cocktail(fetched_cocktail)
        enriched_cocktail['ingredients'] = self.extract_ingredients_from_fetched_cocktail(fetched_cocktail)
        return enriched_cocktail

    def extract_ingredients_from_provided_cocktail(self, provided_cocktail):
        if provided_cocktail is None:
            print('None cocktail provided..')
            return None
        
        cocktail_ingredients = provided_cocktail.get('ingredients')
        if cocktail_ingredients is None:
            print(f'Could not extract ingredients from : {provided_cocktail}')
            return None
        
        if len(cocktail_ingredients) < 1:
            print(f'No ingredients found in : {provided_cocktail}')
            return None
        
        ingredients = {}
        for ingredient in cocktail_ingredients:
            ingredient_name = ingredient.strip()
            thumb = self.create_ingredient_thumbnail(ingredient)
            ingredients[ingredient_name] = {
                'measure': None,
                'thumb': thumb
            }
            
        return ingredients
    
    def extract_instructions_from_fetched_cocktail(self, fetched_cocktail):
        if fetched_cocktail is None:
            print('None cocktail provided..')
            return None
        
        instructions = {}
        for lang in ['', 'es', 'fr', 'de', 'it', 'zh-Hans', 'zh-Hant']:
            lang_inst = fetched_cocktail.get(f'strInstructions{lang.upper()}')
            if lang_inst:
                lang_code = lang if lang else 'en'
                instructions[lang_code] = lang_inst.strip()
                
        return instructions
    
    def extract_ingredients_from_fetched_cocktail(self, fetched_cocktail):
        if fetched_cocktail is None:
            print('None cocktail provided..')
            return None
        
        ingredients = {}
        for i in range(1, 16):
            ingredient = fetched_cocktail.get(f'strIngredient{i}')
            if ingredient:
                ingredient_name = ingredient.strip()
                measure = fetched_cocktail.get(f'strMeasure{i}')
                trimmed_measure = measure.strip() if measure else None
                thumb = self.create_ingredient_thumbnail(ingredient)
                ingredients[ingredient_name] = {
                    'measure': trimmed_measure,
                    'thumb': thumb
                }
                
        return ingredients
    
    def create_ingredient_thumbnail(self, ingredient):
        thumbnail_url = f"https://www.thecocktaildb.com/images/ingredients/{ingredient}.png"
        response = requests.get(thumbnail_url)
        
        if response.status_code != 200:
            print(f"Thumbnail '{thumbnail_url}' is not valid..")
            return None
        
        return thumbnail_url