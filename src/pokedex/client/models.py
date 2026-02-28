from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Pokemon:
    id: int
    name: str
    types: list[str]

    abilities: list["PokemonAbility"] = field(default_factory=list)
    moves: list["PokemonMove"] = field(default_factory=list)
    stats: list["PokemonStat"] = field(default_factory=list)
    sprites: list["PokemonSprites"] = field(default_factory=list)

    cries: Optional["PokemonCries"] = None


@dataclass(frozen=True)
class NamedAPIResource:
    name: str
    url: str


@dataclass(frozen=True)
class APIResource:
    url: str


@dataclass
class move:
    id: int
    name: str
    accuracy: Optional[int]
    effect_chance: Optional[int]
    pp: int
    priority: int
    power: Optional[int]


@dataclass
class PokemonMove:
    move: NamedAPIResource
    # version_group_details: PokemonMoveVersion


@dataclass
class PokemonCries:
    latest: Optional[str]
    legacy: Optional[str]


@dataclass
class PokemonStat:
    stat: NamedAPIResource
    effort: int
    base_stat: int


@dataclass
class PokemonSprites:
    front_default: Optional[str] = None


@dataclass
class PokemonAbility:
    is_hidden: bool
    slot: int
    ability: NamedAPIResource
