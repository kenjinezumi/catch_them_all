# Catch them all

## Description

Application in django to GET all Pokemon names and characteristics from the PokeAPI.

## Prerequisites

Before running the project, you need to have the following installed on your system:

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)
- PostgreSQL
- Python 3.11
- Poetry

## Getting Started

Follow the steps below to run the Django project using Docker.

1. Clone the repository to your local machine:

```bash
git clone https://github.com/kenjinezumi/catch_them_all.git
cd catch_them_all
```
2.  Setup PostgreSQL
```commandline
psql -U postgres
CREATE USER pikachu WITH PASSWORD raichu;
CREATE DATABASE pokemons;
CREATE ROLE pikachu WITH LOGIN PASSWORD 'raichu';
GRANT ALL PRIVILEGES ON DATABASE pokemons TO pikachu;
psql -U pikachu -d pokemons -h localhost -p 5432
```

3. Run Poetry 
```commandline
poetry install 
```

4. Run the migrations
```commandline
poetry run python migrate
```

4. Fetch the Pokemons
```commandline
poetry run python manage.py catch_them_all
```

5. Run the server
```commandline
poetry run python manage.py runserver
```