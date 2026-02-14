class PokeApiError(Exception):
    """Base error for PokeAPI client."""


class PokemonNotFoundError(PokeApiError):
    """Pokemon not found (404)."""


class PokeApiTimeoutError(PokeApiError):
    """Request timed out."""


class PokeApiRateLimitError(PokeApiError):
    """Rate limited by API (429)."""


class PokeApiServerError(PokeApiError):
    """Server-side error (5xx)."""
