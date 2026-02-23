import httpx
import pytest
import respx

from pokedex.client.errors import (
    PokeApiRateLimitError,
    PokeApiServerError,
    PokeApiTimeoutError,
    PokemonNotFoundError,
)
from pokedex.client.models import Pokemon
from pokedex.client.pokeapi import PokeApiClient

POKEAPI_BASE = "https://pokeapi.co/api/v2"


## Estas pruebas verifican que el cliente de PokeAPI maneja correctamente las respuestas
#  exitosas y los errores comunes,#  como 404, 429, 5xx y timeouts. Utilizan respx
# para simular las respuestas de la API # sin hacer llamadas reales a la red.
def _pokemon_payload():
    # Respuesta mínima realista de PokeAPI para /pokemon/{name}
    return {
        "id": 25,
        "name": "pikachu",
        "types": [
            {
                "slot": 1,
                "type": {
                    "name": "electric",
                    "url": "https://pokeapi.co/api/v2/type/13/",
                },
            }
        ],
    }


## Cada prueba utiliza respx para interceptar la solicitud HTTP y devolver una respuesta
#  simulada con el código de estado y el contenido deseados.
@respx.mock
def test_get_pokemon_200_maps_to_dataclass():
    respx.get(f"{POKEAPI_BASE}/pokemon/pikachu").respond(
        status_code=200,
        json=_pokemon_payload(),
    )

    ## Se crea una instancia de PokeApiClient y se llama al método get_pokemon con el
    # nombre "pikachu".     # Luego, se verifican los atributos del objeto Pokemon
    #  #  devuelto para asegurarse de que se hayan mapeado
    #  correctamente desde la respuesta JSON.
    with PokeApiClient() as client:
        p = client.get_pokemon("pikachu")

    ## Se comprueba que el objeto devuelto es una instancia de Pokemon y que sus atributos id,
    #  name y types coinciden con los valores esperados según la respuesta simulada.
    assert isinstance(p, Pokemon)
    assert p.id == 25
    assert p.name == "pikachu"
    assert p.types == ["electric"]


@respx.mock
def test_get_pokemon_404_raises_not_found():
    respx.get(f"{POKEAPI_BASE}/pokemon/pikachooo").respond(status_code=404)

    ## Se crea una instancia de PokeApiClient y se llama al método get_pokemon con un nombre
    #  que no existe ("pikachooo").
    with PokeApiClient() as client:
        ## Se verifica que se lance una excepción PokemonNotFoundError al intentar obtener un
        #  Pokémon que no existe,
        #  lo que indica que el cliente maneja correctamente el error 404 de la API.
        with pytest.raises(PokemonNotFoundError):
            client.get_pokemon("pikachooo")


@respx.mock
def test_get_pokemon_429_raises_rate_limit():
    respx.get(f"{POKEAPI_BASE}/pokemon/pikachu").respond(status_code=429)

    with PokeApiClient() as client:
        with pytest.raises(PokeApiRateLimitError):
            client.get_pokemon("pikachu")


@respx.mock
def test_get_pokemon_5xx_raises_server_error():
    respx.get(f"{POKEAPI_BASE}/pokemon/pikachu").respond(status_code=500)

    with PokeApiClient() as client:
        with pytest.raises(PokeApiServerError):
            client.get_pokemon("pikachu")


@respx.mock
def test_get_pokemon_timeout_raises_timeout_error():
    def _raise_timeout(_request: httpx.Request) -> httpx.Response:
        raise httpx.TimeoutException("boom")

    respx.get(f"{POKEAPI_BASE}/pokemon/pikachu").mock(side_effect=_raise_timeout)

    with PokeApiClient() as client:
        with pytest.raises(PokeApiTimeoutError):
            client.get_pokemon("pikachu")
