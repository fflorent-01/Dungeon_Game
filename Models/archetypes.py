#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Define base archetype for the game

- Archetype -> Contains base data for hero_classes and monster_types types
- Rooster -> Wraps hero_classes and monster_types types Archetype list
- rooster -> Contains the hero_classes and monster_types
"""
from typing import NamedTuple
from dataclasses import dataclass


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
    melee: bool = True
    range: bool = False

    def print(self) -> None:
        separator = "-" * 60
        string_list = [
            separator,
            f"{self.name.upper()}",
            f"Base hit points: {self.base_hp}, Base damage: {self.base_dmg}, Crit chance: {self.crit_chance}",
            f"Base XP: {self.base_xp}" if self.type == "monster" else "",
            f"{'Melee' if self.melee else ''}"
            f"{', ' if self.melee and self.range else ''}"
            f"{'Range' if self.range else ''}"
        ]

        print("\n".join([string for string in string_list if string]))


@dataclass
class Rooster:
    """
    Hold hero_classes and monster_types archetypes together
    """
    hero_classes: list[Archetype]
    monster_types: list[Archetype]


# Hero archetypes
warrior = Archetype("hero", "Warrior", 500, 40)
archer = Archetype("hero", "Archer", 300, 30, crit_chance=25, melee=False, range=True)
ranger = Archetype("hero", "Ranger", 350, 35, range=True)
thief = Archetype("hero", "Thief", 300, 30, crit_chance=35)

hero_classes = [warrior, archer, ranger, thief]

# Monsters archetypes
goblin = Archetype("monster", "Goblin", 200, 10, base_xp=25)
goblin_rogue = Archetype("monster", "Goblin rogue", 140, 25, base_xp=35, crit_chance=35)
goblin_archer = Archetype("monster", "Goblin archer", 125, 20, base_xp=25, crit_chance=15, melee=False, range=True)
hobgoblin = Archetype("monster", "Hobgoblin", 350, 25, base_xp=60, range=True)

monster_types = [goblin, goblin_rogue, goblin_archer, hobgoblin]

# Create Rooster
rooster = Rooster(hero_classes, monster_types)
