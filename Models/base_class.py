#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Base classes
"""

import random
from Models.archetypes import Archetype

class Combatant:
    """
    - Calculates combat stats based on Archetype and level.
    - Provide base combat actions

    """
    def __init__(self, name, archetype, level):
        self.name = name
        self.level = level
        self.hp = level * archetype.base_hp
        self.dmg = int((level + 1) * (archetype.base_dmg / 2))
        self.crit_chance = archetype.crit_chance

    def is_alive(self):
        return self.hp > 0

    def attack(self, opponent):
        damages = int(random.normalvariate(self.dmg, 5))
        crit = random.randint(0, 100) < self.crit_chance
        sum_damages = damages + (crit * int(self.dmg / 2))
        opponent.hp -= sum_damages
        print(
            f"{self.name} deals {sum_damages}. {opponent.name} has {opponent.hp} hp left."
        )
        if opponent.is_alive():
            return
        else:
            self.win()

    def win(self):
        print(f"{self.name} won the battle.")


class Hero(Combatant):
    def __init__(self, name: str, archetype: Archetype, level: int = 1):
        super().__init__(name, archetype, level)
        self.xp: int = 0
        self.nbs_victory: int = 0
        self.monster_killed: list[Monster] = []

    def __repr__(self):
        string = f"Name: {self.name}, Class: {self.name}, Level: {self.level}\n" \
                 f"HP: {self.hp}, Base damage: {self.dmg}, XP: {self.xp}"
        return string


class Monster(Combatant):
    def __init__(self, name, monster_type, level=1):
        self.monster_type = monster_type
        super().__init__(name, level, monster_type.base_hp, monster_type.base_dmg, monster_type.crit_chance)
        self.xp = level * monster_type.base_xp

    def __repr__(self):
        string = f"Name: {self.name}, Class: {self.name}, Level: {self.level}\n" \
                 f"HP: {self.hp}, Base damage: {self.dmg}, XP: {self.xp}"
        return string
