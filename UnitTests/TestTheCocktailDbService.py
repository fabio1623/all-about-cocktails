import unittest
from Services.TheCocktailDbService import TheCocktailDbService

class TestTheCocktailDbService(unittest.TestCase):
    def setUp(self):
        self.the_cocktail_db_service = TheCocktailDbService()
        
    def test_enrich_cocktails(self):
        cocktails = [
            {
                "name": "Cosmopolitan",
                "ingredients": ["Vodka", "Lime juice", "Cointreau", "Cranberry juice"]
            },
            {
                "name": "Gin Mule",
                "ingredients": ["Gin", "Ginger beer", "Lime juice"]
            }
        ]
        enriched_cocktails = self.the_cocktail_db_service.enrich_cocktails(cocktails)
        self.assertTrue(len(enriched_cocktails) > 0)
        
        expected_cosmopolitan = {
            'name': 'Cosmopolitan', 
            'thecocktaildb_id': 17196, 
            'category': 'Cocktail', 
            'iba': 'Contemporary Classics', 
            'alcoholic': 'Alcoholic', 
            'instructions': {
                'en': 'Add all ingredients into cocktail shaker filled with ice. Shake well and double strain into large cocktail glass. Garnish with lime wheel.', 
                'de': 'Alle Zutaten in den mit Eis gefüllten Cocktailshaker geben. Gut schütteln und doppelt in ein großes Cocktailglas abseihen. Mit Limettenrad garnieren.', 
                'it': 'Aggiungi tutti gli ingredienti in uno shaker pieno di ghiaccio.\r\nShakerare bene e filtrare due volte in una grande coppetta da cocktail.\r\nGuarnire con una fetta di lime.'
            }, 
            'glass': 'Cocktail glass', 
            'ingredients': {
                'Vodka': {
                    'measure': '1 1/4 oz', 
                    'thumb': 'https://www.thecocktaildb.com/images/ingredients/Vodka.png'
                }, 
                'Lime juice': {
                    'measure': '1/4 oz', 
                    'thumb': 'https://www.thecocktaildb.com/images/ingredients/Lime juice.png'
                }, 
                'Cointreau': {
                    'measure': '1/4 oz', 
                    'thumb': 'https://www.thecocktaildb.com/images/ingredients/Cointreau.png'
                }, 
                'Cranberry juice': {
                    'measure': '1/4 cup', 
                    'thumb': 'https://www.thecocktaildb.com/images/ingredients/Cranberry juice.png'
                }
            }, 
            'thumb': 'https://www.thecocktaildb.com/images/media/drink/kpsajh1504368362.jpg'
        }
        
        expected_gin_mule = {
            'name': 'Gin Mule', 
            'thecocktaildb_id': None, 
            'category': None, 
            'iba': None, 
            'alcoholic': None, 
            'instructions': None, 
            'glass': None, 
            'ingredients': {
                'Gin': {
                    'measure': None, 
                    'thumb': 'https://www.thecocktaildb.com/images/ingredients/Gin.png'
                }, 
                'Ginger beer': {
                    'measure': None, 
                    'thumb': 'https://www.thecocktaildb.com/images/ingredients/Ginger beer.png'
                }, 
                'Lime juice': {
                    'measure': None, 
                    'thumb': 'https://www.thecocktaildb.com/images/ingredients/Lime juice.png'
                }
            }, 
            'thumb': None
        }
        
        self.assertEqual(enriched_cocktails[0], expected_cosmopolitan)
        self.assertEqual(enriched_cocktails[1], expected_gin_mule)