#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Base classes

- Combatant -> Base class to instantiate Hero and Monster
- Hero -> Instantiate a hero
- Monster -> Instantiate a monster

"""
import random
from Models.archetypes import Archetype


class Combatant:
    """
    - Calculates combat stats based on Archetype and level.
    - Provide base combat actions

    """
    def __init__(self, name: str, archetype: Archetype, level: int):
        # Received
        self.name: str = name
        self.archetype: Archetype = archetype
        self.level: int = level
        # Inferred
        # Combat
        self.hp: int = level * archetype.base_hp
        self.dmg: int = int((level + 1) * (archetype.base_dmg / 2))
        self.crit_chance: int = archetype.crit_chance
        self.melee: bool = archetype.melee
        self.range: bool = archetype.range
        self.combat_range: list[str] = self._set_combat_range()

    def is_alive(self) -> bool:
        return self.hp > 0

    def is_hero(self) -> bool:
        return self.archetype.type == "hero"

    def is_monster(self) -> bool:
        return self.archetype.type == "monster"

    def attack(self, opponent: "Combatant", range_battle: bool, range_atk: bool) -> None:
        if range_battle and not range_atk:
            print(f"{self.name} could not reach {opponent.name}.")
            return
        dmg: int = int(random.normalvariate(self.dmg, 5))
        if range_atk:
            if range_battle:
                dmg = int(dmg * 0.80)
            else:
                dmg = int(dmg * 1.05)
        crit: bool = self._check_crit(range_battle, range_atk)
        sum_damages: int = dmg + (crit * int(self.dmg / 2))  # Effectively means 50% bonus dmg on crit
        self._dmg_opponent(opponent, sum_damages)

    def win(self, opponent: "Combatant"):
        print(f"\n{self.name} won the battle against {opponent.name}.\n")

    def _set_combat_range(self):
        combat_range = []
        if self.melee:
            combat_range.append("melee")
        if self.range:
            combat_range.append("range")
        return combat_range

    def _check_crit(self, range_battle: bool = False, range_atk: bool = False) -> bool:
        crit_chance = self.crit_chance
        if not range_battle and range_atk:
            crit_chance -= 5

        return random.randint(0, 100) <= crit_chance

    def _dmg_opponent(self, opponent: "Combatant", dmg: int) -> None:
        opponent.hp -= dmg
        print(f"{self.name} deals {dmg}. {opponent.name} has {opponent.hp} hp left.")
        if opponent.is_alive():
            return
        else:
            self.win(opponent)

    def print(self) -> None:
        separator = "-" * 60
        string_list = [
            separator,
            f"{self.name.upper()}",
            f"Hit points: {self.hp}, Damage: {self.dmg}, Crit chance: {self.crit_chance}",
            f"Experience points: {self.level * self.archetype.base_xp}" if self.is_monster() else "",
            f"{'Melee' if self.melee else ''}"
            f"{', ' if self.melee and self.range else ''}"
            f"{'Range' if self.range else ''}"
        ]

        print("\n".join([string for string in string_list if string]))


class Monster(Combatant):
    def __init__(self, name: str, archetype: Archetype, level=1):
        super().__init__(name, archetype, level)
        self.xp = level * archetype.base_xp

    def __repr__(self):
        string = f"Name: {self.name}, Level: {self.level}\n" \
                 f"HP: {self.hp}, Base damage: {self.dmg}, XP: {self.xp}"
        return string


class Hero(Combatant):
    def __init__(self, name: str, archetype: Archetype, level: int = 1):
        super().__init__(name, archetype, level)
        self.full_hp: int = self.hp
        self.xp: int = 0
        self.xp_next_level = 100 * level ** 1.5
        self.nbs_victory: int = 0
        self.monster_killed: list[Monster] = []

    def win(self, opponent: Monster):
        super().win(opponent)
        self.nbs_victory += 1
        print(f"You have won {self.nbs_victory} times.")
        self.monster_killed.append(opponent)
        self._add_xp(opponent)

    def _add_xp(self, opponent: Monster):
        self.xp += opponent.xp
        print(f"You just won {opponent.xp}xp. You currently have {self.xp}xp.")
        if self.xp >= self.xp_next_level:
            self._gain_level()
        else:
            print(f"You need {self.xp_next_level-self.xp: .0f} for your next level.")

    def _gain_level(self):
        self.level += 1
        self.xp_next_level = 100 * self.level ** 1.5

        self.full_hp = self.level * self.archetype.base_hp
        self.dmg = int((self.level + 1) * (self.archetype.base_dmg / 2))
        print(f"Congratulation! You just won a level. You are now level {self.level}")
        self.hp = self.full_hp
        self.print()
