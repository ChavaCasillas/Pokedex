import argparse
import json
import logging
import sys
from dataclasses import asdict
from typing import Sequence

from pokedex.client.errors import (
    PokeApiError,
    PokeApiRateLimitError,
    PokeApiServerError,
    PokeApiTimeoutError,
    PokemonNotFoundError,
)
from pokedex.client.pokeapi import PokeApiClient

## Configuro el logger para la aplicación, lo que permitirá registrar mensajes de
logger = logging.getLogger(__name__)

EX_OK = 0
EX_USAGE = 2
EX_NOT_FOUND = 3
EX_NET = 4
EX_RATE_LIMIT = 5
EX_SERVER = 6
EX_UNKNOWN = 1


def build_cli_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="pokedex", description="Pokedex CLI (Phase 1 MVP)")

    parser.add_argument(
        "--log-level",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Set the logging level (default: INFO)",
    )

    sub = parser.add_subparsers(dest="command", required=True)

    # pokedex get <name_or_id>
    get_parser = sub.add_parser("get", help="Get a Pokémon by name or ID")
    get_parser.add_argument("name_or_id", help="Name or ID of the Pokémon")
    get_parser.add_argument(
        "--json", action="store_true", help="Output Pokémon data in JSON format"
    )

    return parser


def cmd_get(args: argparse.Namespace) -> int:
    client = PokeApiClient()

    try:
        pokemon = client.get_pokemon(args.name_or_id)

        if args.json:
            print(json.dumps(asdict(pokemon), ensure_ascii=False, indent=2))
            logger.debug(f"Outputted Pokémon data in JSON format: {pokemon}")
        else:
            print(render_pokemon_human(pokemon))
            logger.debug(f"Outputted Pokémon data in human-readable format: {pokemon}")

        return EX_OK

    except PokemonNotFoundError:
        print(
            f"Error: Pokémon with name or ID '{args.name_or_id}' not found.",
            file=sys.stderr,
        )
        logger.debug("PokemonNotFoundError raised.", exc_info=True)
        return EX_NOT_FOUND

    except PokeApiTimeoutError:
        print(
            "Error: Request to PokeAPI timed out.",
            file=sys.stderr,
        )
        logger.debug("PokeApiTimeoutError raised.", exc_info=True)
        return EX_NET

    except PokeApiRateLimitError:
        print(
            "Error: Rate limit exceeded when calling PokeAPI.",
            file=sys.stderr,
        )
        logger.debug("PokeApiRateLimitError raised.", exc_info=True)
        return EX_RATE_LIMIT

    except PokeApiServerError:
        print(
            "Error: Server error occurred when calling PokeAPI.",
            file=sys.stderr,
        )
        logger.debug("PokeApiServerError raised.", exc_info=True)
        return EX_SERVER

    except PokeApiError:
        print(
            "Error: An unexpected error occurred when calling PokeAPI.",
            file=sys.stderr,
        )
        logger.debug("Generic PokeApiError raised.", exc_info=True)
        return EX_UNKNOWN


def render_pokemon_human(pokemon) -> str:
    """
    Returns a human-readable string representation of a Pokemon.
    This function is responsible ONLY for formatting.
    """

    types_str = ", ".join(pokemon.types)

    return f"Pokemon: {pokemon.name} (#{pokemon.id})\nTypes  : {types_str}"


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_cli_parser()
    args = parser.parse_args(argv)

    # Configure logging
    logging.basicConfig(
        level=getattr(logging, args.log_level), format="%(levelname)s: %(message)s"
    )

    if args.command == "get":
        return cmd_get(args)

    parser.error("Command not implemented")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
