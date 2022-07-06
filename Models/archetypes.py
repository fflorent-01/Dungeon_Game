#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Define base archetype for the game
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
    melee_atk: bool = True
    range_atk: bool = False

    def print(self):
        separator = "-" * 60
        string_list = [
            separator,
            f"{self.name.upper()}",
            f"Base hit points: {self.base_hp}, Base damage: {self.base_dmg}, Crit chance: {self.crit_chance}",
            f"Base XP: {self.base_xp}" if self.type == "monster" else "",
            f"{'Melee' if self.melee_atk else ''}"
            f"{', ' if self.melee_atk and self.range_atk else ''}"
            f"{'Range' if self.range_atk else ''}"
        ]
        # [string for string in string_list if string]
        print("\n".join([string for string in string_list if string]))


@dataclass
class Rooster:
    """
    Hold heroes and monsters archetypes together
    """
    heroes: list[Archetype]
    monsters: list[Archetype]


# Hero archetypes
warrior = Archetype("hero", "Warrior", 500, 20)
archer = Archetype("hero", "Archer", 300, 25, crit_chance=20, melee_atk=False, range_atk=True)
ranger = Archetype("hero", "Ranger", 350, 25, range_atk=True)
thief = Archetype("hero", "Thief", 300, 30, crit_chance=30)

heroes = [warrior, archer, ranger, thief]

# Monsters archetypes
goblin = Archetype("monster", "Goblin", 200, 10, base_xp=25)
goblin_rogue = Archetype("monster", "Goblin rogue", 140, 25, base_xp=35, crit_chance=35)
goblin_archer = Archetype("monster", "Goblin archer", 125, 20, base_xp=25, crit_chance=15,
                          melee_atk=False, range_atk=True)
hobgoblin = Archetype("monster", "Hobgoblin", 400, 25, base_xp=60, range_atk=True)

monsters = [goblin, goblin_rogue, goblin_archer, hobgoblin]

# Create Rooster
rooster = Rooster(heroes, monsters)
