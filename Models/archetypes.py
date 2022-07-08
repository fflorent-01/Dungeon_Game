#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Define base archetype for the game

- Archetype -> Contains base data for hero_classes and monster_types types
- Rooster -> Wraps hero_classes and monster_types types Archetype list
- rooster -> Contains the hero_classes and monster_types
"""
from enum import Enum, auto
from typing import NamedTuple, Optional
from dataclasses import dataclass


class RangeType(Enum):
    RANGE: str = "range"
    MELEE: str = "melee"


class Archetype(NamedTuple):
    """
    Base archetype used to create character classes and monster types.
    """
    type: str
    name: str
    base_hp: int
    base_dmg: int
    crit_chance: int = 10
    base_xp: int = 0
    available_range: list[RangeType] = [RangeType.MELEE]
    preferred_range: Optional[RangeType] = None  # Unused at the moment

    def print(self) -> None:
        """Print the archetype basic stats."""
        separator = "-" * 60
        string_list = [
            separator,
            f"{self.name.upper()}",
            f"Base hit points: {self.base_hp}, Base damage: {self.base_dmg}, Crit chance: {self.crit_chance}",
            f"Base XP: {self.base_xp}" if self.type == "monster" else "",
            f"{'Melee' if RangeType.MELEE in self.available_range else ''}"
            f"{', ' if len(self.available_range) > 1 else ''}"
            f"{'Range' if RangeType.RANGE in self.available_range else ''}"
        ]

        print("\n".join([string for string in string_list if string]))


@dataclass
class Rooster:
    """
    Hold hero_classes and monster_types archetypes together
    """
    hero_classes: list[Archetype]
    monster_types: list[Archetype]


# Initialization of hero classes and monster types
# Could probably be improved for external import, but I keep like this for readability

rooster = Rooster(
    # Hero archetypes
    [
        Archetype("hero", "Warrior", 500, 40),
        Archetype("hero", "Archer", 300, 30, crit_chance=25, available_range=[RangeType.RANGE]),
        Archetype("hero", "Ranger", 350, 35, available_range=[RangeType.MELEE, RangeType.RANGE]),
        Archetype("hero", "Thief", 300, 30, crit_chance=35),
    ],
    # Monster archetypes
    [
        Archetype("monster", "Goblin", 200, 10, base_xp=25),
        Archetype("monster", "Goblin rogue", 140, 25, base_xp=35, crit_chance=35),
        Archetype("monster", "Goblin archer", 125, 20, base_xp=25, crit_chance=15, available_range=[RangeType.RANGE]),
        Archetype("monster", "Hobgoblin", 350, 25, base_xp=60, available_range=[RangeType.MELEE, RangeType.RANGE],
                  preferred_range=RangeType.MELEE),
    ]
)
