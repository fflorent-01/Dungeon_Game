#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Game object: main feature
"""
from random import choice
from typing import Optional

from Models import Rooster, rooster, Hero, Monster, RangeType
from DistUtils import *


class Game:
    rooster: Rooster = rooster
    # Selectors helper
    hero_selector: dict[str, Archetype] = create_selection_dict(rooster.hero_classes, "name")
    hero_selection_description: str = create_selection_description(rooster.hero_classes, "name")
    monster_selector: dict[str, Archetype] = create_selection_dict(rooster.monster_types, "name")
    monster_selection_description: str = create_selection_description(rooster.monster_types, "name")

    def __init__(self) -> None:
        self.hero: Hero
        self.monster: Monster
        self.combat_range: Optional[RangeType] = None
        self.hero_atk_range: Optional[RangeType] = None
        self.monster_atk_range: Optional[RangeType] = None

    def start(self) -> None:
        print('Welcome to my game!')
        self.run()

    def restart(self) -> None:
        self.run()

    def run(self) -> None:
        self._select_hero()
        print("Your enter a cavern.")
        print("You venture into a tunnel until you encounter:")
        press_to_continue()
        keep_going: bool = True
        while keep_going and self.hero.is_alive():
            self._select_monster()
            press_to_continue()
            # I should probably break down combat / round into separate classes - would isolate a lot of fucntions
            while self.monster.is_alive() and self.hero.is_alive():
                self.combat_range, self.hero_atk_range, self.monster_atk_range = self._select_range_and_atk()
                self.hero.attack(self.monster, self.combat_range, self.hero_atk_range)
                if self.monster.is_alive():
                    self.monster.attack(self.hero, self.combat_range, self.monster_atk_range)
                if len(self.hero.available_range) == 1:
                    press_to_continue()

            if not self.hero.is_alive():
                box_msg("Too bad you are dead!")
            else:
                keep_going = ask_continue()
                self.hero.hp = self.hero.full_hp
                print("You heal yourself and venture further into the tunnel until you encounter:\n")

        if self.hero.is_alive():
            box_msg("Congratulation, you retired!")

        if ask_yes_no("Do you want to start over?"):
            self.restart()

    def _select_hero(self) -> None:
        """Prompt questions to generate a new hero and create it."""
        hero_name = input("Please write your hero name: ")
        for hero in rooster.hero_classes:
            hero.print()
        hero_type: Archetype = ask_selection("Please select your hero class.",
                                             self.hero_selector, self.hero_selection_description)
        self.hero = Hero(hero_name, hero_type)
        print("You have successfully created your hero.")
        self.hero.print()
        press_to_continue()

    def _select_monster(self):
        """Selects a monster from the rooster and create it."""
        chosen_monster = choice([k for k in self.monster_selector.keys()])
        monster_type: Archetype = self.monster_selector[chosen_monster]
        self.monster = Monster(monster_type.name, monster_type, self.hero.level)
        self.monster.print()

    def _select_hero_range(self, string: str) -> RangeType:
        """Select or prompt for a range for the hero."""
        if len(self.hero.available_range) == 1:
            return self.hero.available_range[0]
        answer_choices: dict = create_selection_dict(self.hero.available_range, "value")
        answer_description: str = create_selection_description(self.hero.available_range, "value")

        return ask_selection(string, answer_choices, answer_description)

    def _select_monster_range(self) -> RangeType:
        """Selects a range for the monster"""
        if len(self.monster.available_range) == 1:
            return self.monster.available_range[0]

        return choice(self.monster.available_range)

    def _select_range_and_atk(self) -> list[RangeType]:
        """Determine the combat and attack range for the round."""
        hero_combat_range: RangeType = self._select_hero_range("\nAt what RANGE do you want to attack?")
        hero_atk_range: RangeType = self._select_hero_range("\nWhat KIND of attack do you want to perform?")
        monster_combat_range: RangeType = self._select_monster_range()
        monster_atk_range: RangeType = self._select_monster_range()
        combat_range: RangeType = hero_combat_range
        if hero_combat_range != monster_combat_range:
            combat_range = choice([hero_combat_range, monster_combat_range])
        print(f"\nThe round range is {combat_range.value}, you will be performing a {hero_atk_range.value} attack "
              f"and the {self.monster.name} a {monster_atk_range.value} attack.")
        return [combat_range, hero_atk_range, monster_atk_range]


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    game = Game()
    game.start()


