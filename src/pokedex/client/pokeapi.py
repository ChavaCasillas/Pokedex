import httpx

### Importo los modelos y errores personalizados para manejar las respuestas de la API
#  y los posibles errores que puedan ocurrir durante las solicitudes.
from .errors import (
    PokeApiError,
    PokemonNotFoundError,
    PokeApiTimeoutError,
    PokeApiRateLimitError,
    PokeApiServerError,
)
from .models import Pokemon


### se crea la clase PokeApiClient que se encargará de interactuar con la API de
# PokeAPI.# Esta clase tiene un método get_pokemon que toma el nombre de un
# Pokémon y devuelve un
# objeto Pokemon con su información.


class PokeApiClient:
    BASE_URL = "https://pokeapi.co/api/v2"

    def __init__(self, timeout: float = 5.0) -> None:
        self._client = httpx.Client(
            base_url=self.BASE_URL,
            timeout=timeout,
            headers={"Accept": "application/json"},
        )

    def close(self) -> None:
        self._client.close()

    def __enter__(self) -> None:
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def get_pokemon(self, name_or_id: str | int) -> Pokemon:
        ## Realizo la solicitud GET a la API de PokeAPI para obtener la información
        #  del Pokémon especificado por su nombre o ID.
        try:
            response = self._client.get(f"/pokemon/{name_or_id}")
        ##  Manejo explícito de excepciones relacionadas con la red y el tiempo
        #  de espera utilizando httpx.
        except httpx.TimeoutException as e:
            raise PokeApiTimeoutError() from e
        except httpx.RequestError as e:
            raise PokeApiError("Network error while calling PokeAPI") from e

        # Manejo explícito de códigos HTTP
        if response.status_code == 404:
            raise PokemonNotFoundError(str(name_or_id))
        if response.status_code == 429:
            raise PokeApiRateLimitError()
        if 500 <= response.status_code < 600:
            raise PokeApiServerError()
        if response.status_code >= 400:
            raise PokeApiError(f"Unexpected HTTP error {response.status_code}")

        data = response.json()
        ## Extraigo los tipos del Pokémon de la respuesta JSON y los almaceno en una lista.

        types = []

        ## La respuesta de la API tiene una estructura específica para los tipos, por lo
        #  que itero sobre la lista de tipos
        # y extraigo el nombre de cada tipo para construir la lista de tipos del Pokémon.
        for item in data.get("types", []):
            type_info = item["type"]
            type_name = type_info["name"]
            types.append(type_name)

        ## Finalmente, creo y devuelvo un objeto Pokemon utilizando los datos extraídos de
        # clela respuesta JSON, incluyendo el ID,
        # el nombre y la lista de tipos del Pokémon.

        return Pokemon(
            id=int(data["id"]),
            name=str(data["name"]),
            types=types,
        )
