import json
import pokedex.cli as cli
from pokedex.client.models import Pokemon


def test_get_pokemon_human_output(monkeypatch, capsys):

    ## The monkeypatch fixture is used to replace the get_pokemon method of the
    # PokeApiClient with a mock function that returns a predefined Pokemon object.
    # The capsys fixture is used to capture the output printed to the console during the test.

    ## 1. Fake get_pokemon method that returns a predefined Pokemon object for testing purposes.
    def fake_get_pokemon(self, name_or_id: str) -> Pokemon:
        return Pokemon(id=1, name="bulbasaur", types=["grass", "poison"])
    
    ## 2. Use monkeypatch to replace the get_pokemon method of PokeApiClient with the fake implementation.
    monkeypatch.setattr(cli.PokeApiClient, "get_pokemon", fake_get_pokemon)

    ## 3. Call the cmd_get function with arguments to get the Pokémon "bulbasaur" and capture the output.
    code = cli.main(["get", "bulbasaur"])
    
    ## 4. We capture the output printed to the console and assert that it contains the expected information about the Pokémon.
    captured = capsys.readouterr()

    ## 5 . Assert that the exit code is EX_OK and that the output contains the expected information about the Pokémon.
    assert code == cli.EX_OK
    assert "Pokemon: bulbasaur" in captured.out
    assert "#1" in captured.out
    assert "Types" in captured.out
    assert "grass" in captured.out
    assert "poison" in captured.out
    assert captured.err == ""


def test_get_json_output_success(monkeypatch, capsys):
    # Fake response (sin HTTP real)
    def fake_get_pokemon(self, name_or_id: str):
        return Pokemon(id=7, name="squirtle", types=["water"])

    monkeypatch.setattr(cli.PokeApiClient, "get_pokemon", fake_get_pokemon)

    # Ejecutamos CLI como si fuera terminal
    code = cli.main(["get", "7", "--json"])

    captured = capsys.readouterr()

    # Exit code correcto
    assert code == cli.EX_OK

    # Validamos que stdout sea JSON válido
    payload = json.loads(captured.out)

    assert payload["id"] == 7
    assert payload["name"] == "squirtle"
    assert payload["types"] == ["water"]

    # No debe haber errores
    assert captured.err == ""