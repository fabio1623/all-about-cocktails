# all-about-cocktails

## Configuring the Database Connection

Before running the application, you will need to configure the database connection. To do so, follow these steps:

- Open the docker-compose.yml file in your preferred text editor.
- Look for the environment section for the db service.
- Update the values for `POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB and ports binding` to your preferred values.
- Save the changes to the docker-compose.yml file.
- Once you have updated the docker-compose.yml file, you can start the Docker containers and run the application as described in the previous sections.

## Getting Started

To get started with this project, follow these steps:

- Clone the repository onto your local machine.
- Install pipenv by running `pip install pipenv`.
- Install project dependencies by running `pipenv install`.
- Start the Docker containers by running `docker-compose up -d`.
- Run the application with `pipenv run python program.py`.

## Running Tests

This project includes a suite of unit tests. To run these tests, follow these steps:

- Ensure that the Docker containers are running by running `docker-compose up -d`.
- Run the unit tests with `pipenv run python -m unittest UnitTests/[TestFile].py`.

## Services

This project includes 3 services. Here's a brief overview of each service:

- NexibleService: A service for interacting with the Nexible API.
- PostgreSqlService: A service for connecting to and querying a PostgreSQL database.
- TheCocktailDbService: A service for enriching cocktail data through the CocktailDB API.
