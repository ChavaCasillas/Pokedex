import pytest

from pokedex.client.errors import (
    PokeApiError,
    PokeApiRateLimitError,
    PokeApiServerError,
    PokeApiTimeoutError,
    PokemonNotFoundError,
)


def test_errors_inherit_from_base():
    assert issubclass(PokemonNotFoundError, PokeApiError)
    assert issubclass(PokeApiTimeoutError, PokeApiError)
    assert issubclass(PokeApiRateLimitError, PokeApiError)
    assert issubclass(PokeApiServerError, PokeApiError)


def test_can_raise_and_catch_specific_error():
    with pytest.raises(PokemonNotFoundError):
        raise PokemonNotFoundError("pikachu")


def test_can_catch_any_pokeapi_error():
    with pytest.raises(PokeApiError):
        raise PokeApiTimeoutError()
