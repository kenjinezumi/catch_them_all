from django.core.management.base import BaseCommand
from pokemon.services.pokemon_service import PokemonService

class Command(BaseCommand):
    help = 'Fetches and saves all Pokémon data from the PokeAPI to the database'

    def handle(self, *args, **options):
        self.stdout.write('Fetching all Pokémon data from the PokeAPI...')
        pokemons = PokemonService.get_all_pokemons()

        for pokemon_data in pokemons:
            pokemon_id = pokemon_data['id']
            self.stdout.write(f'Saving data for Pokémon with ID {pokemon_id}...')
            PokemonService.save_new_pokemon(pokemon_id)

        self.stdout.write(self.style.SUCCESS('You catched them all!!!! やった! やった! やった! やった!'))
