import psycopg2
from psycopg2.extras import Json

class PostgreSqlService:
    def __init__(self, postgresql_dbname, dbname, user, password, host, port):
        self.conn = psycopg2.connect(
            dbname=postgresql_dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )
        self.conn.autocommit = True

        # Create the database if it does not exist
        cursor = self.conn.cursor()
        cursor.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{dbname}'")
        exists = cursor.fetchone()
        if not exists:
            cursor.execute(f"CREATE DATABASE {dbname}")
        cursor.close()

        # Connect to the new database
        self.conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )
        
        # Create the cocktails, ingredients, and cocktail_ingredients tables if they do not exist
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cocktails (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL UNIQUE,
                thecocktaildb_id INT,
                category VARCHAR(255),
                iba VARCHAR(255),
                alcoholic VARCHAR(255),
                instructions JSON,
                glass VARCHAR(255),
                thumb VARCHAR(255),
                created_at TIMESTAMP DEFAULT NOW()
            );
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ingredients (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL UNIQUE,
                thumb VARCHAR(255),
                created_at TIMESTAMP DEFAULT NOW()
            );
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cocktail_ingredients (
                id SERIAL PRIMARY KEY,
                cocktail_id INTEGER NOT NULL REFERENCES cocktails(id),
                ingredient_id INTEGER NOT NULL REFERENCES ingredients(id),
                measure VARCHAR(255),
                created_at TIMESTAMP DEFAULT NOW(),
                UNIQUE(cocktail_id, ingredient_id)
            );
        """)
        
        cursor.close()
        
    def create_cocktail(self, cocktail):
        cursor = self.conn.cursor()

        cursor.execute("""
            SELECT id FROM cocktails WHERE name = %s;
        """, (cocktail['name'],))
        row = cursor.fetchone()
        if row:
            cocktail_id = row[0]
        else:
            cursor.execute("""
                INSERT INTO cocktails (name, thecocktaildb_id, category, iba, alcoholic, instructions, glass, thumb)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id;
            """, (cocktail['name'], cocktail['thecocktaildb_id'], cocktail['category'], cocktail['iba'], cocktail['alcoholic'], Json(cocktail['instructions']), cocktail['glass'], cocktail['thumb']))
            cocktail_id = cursor.fetchone()[0]

        for ingredient, properties in cocktail['ingredients'].items():
            cursor.execute("""
                SELECT id FROM ingredients WHERE name = %s;
            """, (ingredient,))
            row = cursor.fetchone()
            if row:
                ingredient_id = row[0]
            else:
                cursor.execute("""
                    INSERT INTO ingredients (name, thumb)
                    VALUES (%s, %s)
                    RETURNING id;
                """, (ingredient, properties['thumb']))
                ingredient_id = cursor.fetchone()[0]

            cursor.execute("""
                INSERT INTO cocktail_ingredients (cocktail_id, ingredient_id, measure)
                VALUES (%s, %s, %s)
                ON CONFLICT (cocktail_id, ingredient_id)
                DO NOTHING;
            """, (cocktail_id, ingredient_id, properties['measure']))

        self.conn.commit()
        cursor.close()

