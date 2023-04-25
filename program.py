from Services.NexibleService import NexibleService
from Services.TheCocktailDbService import TheCocktailDbService
from Services.PostgreSqlService import PostgreSqlService
import getpass

nexible_service = NexibleService()
the_cocktail_db_service = TheCocktailDbService()

postgresql_dbname = input("Enter postgresql_dbname: ")
dbname = input("Enter dbname: ")
user = getpass.getpass("Enter user: ")
password = getpass.getpass("Enter password: ")
host = input("Enter host: ")
port = input("Enter port: ")

postgresql_service = PostgreSqlService(postgresql_dbname, dbname, user, password, host, port)

cocktails = nexible_service.get_cocktails()
cocktails = the_cocktail_db_service.enrich_cocktails(cocktails)

print(f"{len(cocktails)} cocktail(s) enriched.")

[postgresql_service.create_cocktail(cocktail) for cocktail in cocktails]
print('Cocktails added in PostgreSQL.')
