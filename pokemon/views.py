from django.http import JsonResponse
from django.views import View
from django.shortcuts import render
from .services.pokemon_service import PokemonService

class PokemonListView(View):
    def get(self, request):
        pokemons = PokemonService.get_all_pokemons()
        return JsonResponse(pokemons, safe=False)

class PokemonDetailView(View):
    def get(self, request, pk):
        pokemon = PokemonService.get_pokemon(pk)
        if not pokemon:
            return JsonResponse({'error': 'Pokemon not found'}, status=404)
        return JsonResponse(pokemon)

def search_pokemon(request):
    search_term = request.GET.get('q', '')
    results = PokemonService.search_pokemon(search_term)
    if results:
        return JsonResponse(results, safe=False)
    else:
        return JsonResponse({}, status=404)

def random_pokemon(request):
    random_pokemon = PokemonService.random_pokemon()
    if random_pokemon:
        return JsonResponse(random_pokemon)
    else:
        return JsonResponse({}, status=404)

def home(request):
    return render(request, 'search.html')