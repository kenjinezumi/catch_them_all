import pytest
from unittest.mock import patch, Mock

from pokemon.models import Pokemon
from pokemon.services.pokemon_service import PokemonService


@pytest.fixture
def mock_response():
    response_mock = Mock()
    response_mock.status_code = 200
    response_mock.json.return_value = {
        'results': [{'name': 'pokemon1'}, {'name': 'pokemon2'}],
        'next': None
    }
    return response_mock

@pytest.fixture
def mock_pokemon_data():
    return {
        'id': 1,
        'name': 'Charizard',
        'abilities': ['Blaze', 'Solar Power'],
        'types': ['Fire', 'Flying'],
        'stats': {
            'hp': 78,
            'attack': 84,
            'defense': 78,
            'special-attack': 109,
            'special-defense': 85,
            'speed': 100,
        }
    }

@pytest.fixture
def mock_pokemon_objects():
    pokemon1 = Pokemon(id=1, name='pokemon1', abilities=['ability1'], types=['type1'], stats={'hp': 100})
    pokemon2 = Pokemon(id=2, name='pokemon2', abilities=['ability2'], types=['type2'], stats={'hp': 80})
    return [pokemon1, pokemon2]

@pytest.mark.parametrize('mock_pokemon_objects', [[
    Pokemon(id=1, name='pokemon1', abilities=['ability1'], types=['type1'], stats={'hp': 100}),
    Pokemon(id=2, name='pokemon2', abilities=['ability2'], types=['type2'], stats={'hp': 80}),
]], indirect=True)
@patch('requests.get')
def test_get_all_pokemons(mock_get, mock_response, mock_pokemon_objects):
    mock_get.return_value = mock_response
    pokemons = PokemonService.get_all_pokemons()
    expected_pokemons = [
        {'id': mock_pokemon_objects[0].id, 'name': mock_pokemon_objects[0].name},
        {'id': mock_pokemon_objects[1].id, 'name': mock_pokemon_objects[1].name},
    ]
    assert pokemons == expected_pokemons

@patch('requests.get')
def test_get_pokemon(mock_get, mock_response, mock_pokemon_data):
    mock_get.return_value = mock_response
    with patch('pokemon.models.Pokemon.objects.get', return_value=Pokemon(**mock_pokemon_data)):
        pokemon = PokemonService.get_pokemon(1)
        assert pokemon == mock_pokemon_data

def test_get_pokemon_not_found():
    with patch('pokemon.models.Pokemon.objects.get', side_effect=Pokemon.DoesNotExist):
        pokemon = PokemonService.get_pokemon(1)
        assert pokemon is None

@pytest.mark.django_db
@patch('requests.get')
def test_save_new_pokemon(mock_get, mock_response, mock_pokemon_data):
    mock_get.return_value = mock_response
    with patch('pokemon.models.Pokemon.objects.get_or_create', return_value=(Pokemon(**mock_pokemon_data), True)):
        result = PokemonService.save_new_pokemon(1)
        assert result is True

@pytest.mark.django_db
@patch('requests.get')
def test_save_existing_pokemon(mock_get, mock_response, mock_pokemon_data):
    mock_get.return_value = mock_response
    with patch('pokemon.models.Pokemon.objects.get_or_create', return_value=(Pokemon(**mock_pokemon_data), False)):
        result = PokemonService.save_new_pokemon(1)
        assert result is True

def test_save_new_pokemon_not_found():
    with patch('requests.get') as mock_get:
        mock_get.return_value = Mock(status_code=404)
        result = PokemonService.save_new_pokemon(1)
        assert result is False

@pytest.mark.parametrize('mock_pokemon_objects', [[
    Pokemon(id=1, name='pokemon1', abilities=['ability1'], types=['type1'], stats={'hp': 100}),
    Pokemon(id=2, name='pokemon2', abilities=['ability2'], types=['type2'], stats={'hp': 80}),
]], indirect=True)
def test_search_pokemon(mock_pokemon_objects):
    results = PokemonService.search_pokemon('pokemon')
    expected_results = [
        {
            'id': mock_pokemon_objects[0].id,
            'name': mock_pokemon_objects[0].name,
            'abilities': mock_pokemon_objects[0].abilities,
            'types': mock_pokemon_objects[0].types,
            'stats': mock_pokemon_objects[0].stats,
        },
        {
            'id': mock_pokemon_objects[1].id,
            'name': mock_pokemon_objects[1].name,
            'abilities': mock_pokemon_objects[1].abilities,
            'types': mock_pokemon_objects[1].types,
            'stats': mock_pokemon_objects[1].stats,
        },
    ]
    assert results == expected_results

@pytest.mark.parametrize('mock_pokemon_objects', [[
    Pokemon(id=1, name='pokemon1', abilities=['ability1'], types=['type1'], stats={'hp': 100}),
    Pokemon(id=2, name='pokemon2', abilities=['ability2'], types=['type2'], stats={'hp': 80}),
]], indirect=True)
def test_random_pokemon(mock_pokemon_objects):
    with patch('pokemon.models.Pokemon.objects.order_by', return_value=Mock(first=Mock(return_value=mock_pokemon_objects[0]))):
        random_pokemon = PokemonService.random_pokemon()
        assert random_pokemon == {
            'id': mock_pokemon_objects[0].id,
            'name': mock_pokemon_objects[0].name,
            'abilities': mock_pokemon_objects[0].abilities,
            'types': mock_pokemon_objects[0].types,
            'stats': mock_pokemon_objects[0].stats,
        }

def test_random_pokemon_not_found():
    with patch('pokemon.models.Pokemon.objects.order_by', return_value=Mock(first=Mock(return_value=None))):
        random_pokemon = PokemonService.random_pokemon()
        assert random_pokemon is None
