import requests
from pokemon.models import Pokemon

class PokemonService:
    POKEAPI_BASE_URL = 'https://pokeapi.co/api/v2/pokemon'

    @staticmethod
    def get_all_pokemons():
        pokemons = []
        next_page = PokemonService.POKEAPI_BASE_URL

        while next_page:
            response = requests.get(next_page)
            if response.status_code == 200:
                data = response.json()
                results = data['results']
                pokemons.extend([{'id': idx + 1, 'name': pokemon['name']} for idx, pokemon in enumerate(results)])

                next_page = data['next']
            else:
                break

        return pokemons

    @staticmethod
    def get_pokemon(pk):
        pokeapi_url = f'{PokemonService.POKEAPI_BASE_URL}/{pk}'
        response = requests.get(pokeapi_url)

        if response.status_code == 200:
            data = response.json()
            pokemon = {
                'id': data['id'],
                'name': data['name'],
                'abilities': [ability['ability']['name'] for ability in data['abilities']],
                'types': [type_data['type']['name'] for type_data in data['types']],
                'stats': {stat_data['stat']['name']: stat_data['base_stat'] for stat_data in data['stats']},
            }
            return pokemon
        else:
            return None

    @staticmethod
    def save_new_pokemon(pk):
        pokeapi_url = f'{PokemonService.POKEAPI_BASE_URL}/{pk}'
        response = requests.get(pokeapi_url)

        if response.status_code == 200:
            data = response.json()
            abilities = [ability['ability']['name'] for ability in data['abilities']]
            types = [type_data['type']['name'] for type_data in data['types']]
            stats = {stat_data['stat']['name']: stat_data['base_stat'] for stat_data in data['stats']}

            pokemon, created = Pokemon.objects.get_or_create(
                name=data['name'],
                defaults={
                    'pokemon_id': data['id'],
                    'abilities': abilities,
                    'types': types,
                    'stats': stats,
                }
            )

            if not created:
                # Update existing Pokémon data if it already exists
                pokemon.pokemon_id = data['id']
                pokemon.abilities = abilities
                pokemon.types = types
                pokemon.stats = stats
                pokemon.save()

            return True
        else:
            return False

    @staticmethod
    def search_pokemon(search_term):
        results = Pokemon.objects.filter(name__icontains=search_term)[:10]  # Return up to 10 matching Pokémon
        data = [{
                'id': pokemon.id,
                'name': pokemon.name,
                'abilities': pokemon.abilities,
                'types': pokemon.types,
                'stats': pokemon.stats,
            } for pokemon in results]
        print(data)
        return data

    @staticmethod
    def random_pokemon():
        random_pokemon = Pokemon.objects.order_by('?').first()  # Get a random Pokémon
        if random_pokemon:
            data = {
                'id': random_pokemon.id,
                'name': random_pokemon.name,
                'abilities': random_pokemon.abilities,
                'types': random_pokemon.types,
                'stats': random_pokemon.stats,
            }
            return data
        else:
            return None
