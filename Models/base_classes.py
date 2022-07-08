#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Base classes

- Combatant -> Base class to instantiate Hero and Monster
- Hero -> Instantiate a hero
- Monster -> Instantiate a monster

"""
import random
from Models import Archetype, RangeType
from typing import Optional, TypeVar


T_Combatant = TypeVar("T_Combatant", bound="Combatant")  # Ugly, but accepted work around for typing preload type.


class Combatant:
    """
    - Calculates combat stats based on Archetype and level.
    - Provide basic functionality and actions.

    """
    def __init__(self, name: str, archetype: Archetype, level: int):
        # Received
        self.name: str = name
        self.archetype: Archetype = archetype
        self.level: int = level
        self.available_range: list[RangeType] = archetype.available_range
        self.preferred_range: Optional[RangeType] = archetype.preferred_range
        # Inferred
        self.hp: int = level * archetype.base_hp
        self.dmg: int = int((level + 1) * (archetype.base_dmg / 2))
        self.crit_chance: int = archetype.crit_chance

    def is_alive(self) -> bool:
        return self.hp > 0

    def is_hero(self) -> bool:
        return self.archetype.type == "hero"

    def is_monster(self) -> bool:
        return self.archetype.type == "monster"

    def attack(self, opponent: T_Combatant, combat_range: RangeType, atk_range: RangeType) -> None:
        """Execute the attack. Should probably be broken down."""
        # Check if able to attack opponent
        if combat_range == RangeType.RANGE and not atk_range == RangeType.RANGE:
            print(f"{self.name} could not reach {opponent.name}.")
            return
        # Calculate damages according to range
        dmg: int = int(random.normalvariate(self.dmg, 5))
        if atk_range == RangeType.RANGE:
            if combat_range == RangeType.RANGE:
                dmg = int(dmg * 0.80)
            else:
                dmg = int(dmg * 1.05)
        # Calculates crit damages if applicable
        crit: bool = self._check_crit(combat_range, atk_range)
        sum_damages: int = dmg + (crit * int(self.dmg / 2))  # Effectively means 50% bonus dmg on crit
        # Deals damages
        self._dmg_opponent(opponent, sum_damages)

    def win(self, opponent: T_Combatant) -> None:
        print(f"\n{self.name} won the battle against {opponent.name}.\n")

    def _check_crit(self, battle_range: RangeType, atk_range: RangeType) -> bool:
        """Check if attack is a critical hit or not, accounting for range of combat and range of attack."""
        crit_chance = self.crit_chance
        if battle_range == RangeType.MELEE and atk_range == RangeType.RANGE:
            crit_chance -= 5

        return random.randint(0, 100) <= crit_chance

    def _dmg_opponent(self, opponent: T_Combatant, dmg: int) -> None:
        opponent.hp -= dmg
        print(f"{self.name} deals {dmg}. {opponent.name} has {opponent.hp} hp left.")
        if opponent.is_alive():
            return
        else:
            self.win(opponent)

    def print(self) -> None:
        """Print the combatant stats."""
        separator = "-" * 60
        string_list = [
            separator,
            f"{self.name.upper()}",
            f"Hit points: {self.hp}, Damage: {self.dmg}, Crit chance: {self.crit_chance}",
            f"Experience points: {self.level * self.archetype.base_xp}" if self.is_monster() else "",
            f"{'Melee' if RangeType.MELEE in self.available_range else ''}"
            f"{', ' if len(self.available_range) > 1 else ''}"
            f"{'Range' if RangeType.RANGE in self.available_range else ''}"
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

    def win(self, opponent: Monster) -> None:
        """Action to trigger upon hero victory."""
        super().win(opponent)
        self.nbs_victory += 1
        print(f"You have won {self.nbs_victory} times.")
        self.monster_killed.append(opponent)
        self._add_xp(opponent)

    def _add_xp(self, opponent: Monster) -> None:
        """Add XP gain and check for level up."""
        self.xp += opponent.xp
        print(f"You just won {opponent.xp}xp. You currently have {self.xp}xp.")
        if self.xp >= self.xp_next_level:
            self._gain_level()
        else:
            print(f"You need {self.xp_next_level-self.xp: .0f} for your next level.")

    def _gain_level(self) -> None:
        """Add level and adjust stats based on new level."""
        self.level += 1
        self.xp_next_level = 100 * self.level ** 1.5

        self.full_hp = self.level * self.archetype.base_hp
        self.dmg = int((self.level + 1) * (self.archetype.base_dmg / 2))
        print(f"Congratulation! You just won a level. You are now level {self.level}")
        self.hp = self.full_hp
        self.print()
