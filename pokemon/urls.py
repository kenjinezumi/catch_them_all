from django.urls import path
from .views import PokemonListView, PokemonDetailView, home, random_pokemon, search_pokemon
from django.contrib import admin

urlpatterns = [
    path('pokemons/', PokemonListView.as_view(), name='pokemon-list'),
    path('pokemons/<int:pk>/', PokemonDetailView.as_view(), name='pokemon-detail'),
    path('', home, name='home'),
    path('random-pokemon/', random_pokemon, name='random_pokemon'),
    path('search-pokemon/', search_pokemon, name='search_pokemon'),
    path('admin/', admin.site.urls),

]