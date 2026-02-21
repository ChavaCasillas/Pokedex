import argparse
import logging
import json
from dataclasses import asdict
from typing import Sequence
from pokedex.client.errors import (
    PokeApiError,
    PokeApiRateLimitError,
    PokeApiServerError,
    PokeApiTimeoutError,
    PokemonNotFoundError,
)
from pokedex.client.models import Pokemon
from pokedex.client.pokeapi import PokeApiClient




def main(argv: list[str] | None = None) -> int:

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

