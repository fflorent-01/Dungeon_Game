#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Game object: main feature
"""
from random import choice
from Models.archetypes import Archetype, Rooster, rooster
from Models.base_classes import Hero, Monster
from DistUtils.selectors_utils import type_selector, type_selection_description, generate_answer_selector, \
    generate_answer_selector_description
from DistUtils.print_utils import warning_msg, box_msg
from DistUtils.prompt_utils import ask_selection, ask_continue, press_to_continue


class Game:
    rooster: Rooster = rooster
    # Selectors helper
    hero_selector: dict[str, Archetype] = type_selector(rooster.hero_classes)
    hero_selection_description: str = type_selection_description(rooster.hero_classes)
    monster_selector: dict[str, Archetype] = type_selector(rooster.monster_types)
    monster_selection_description: str = type_selection_description(rooster.monster_types)

    def __init__(self) -> None:
        self.hero: Hero
        self.monster: Monster
        self.range_combat: bool = False
        self.hero_range_atk: bool = False
        self.monster_range_atk: bool = False

    def start(self) -> None:
        print('Welcome to my game!')
        self.run()

    def restart(self):
        self.run()

    def run(self):
        self._select_hero()
        print("Your enter a cavern.")
        print("You venture into a tunnel until you encounter:")
        press_to_continue()
        keep_going: bool = True
        while keep_going and self.hero.is_alive():
            self._select_monster()
            press_to_continue()
            while self.monster.is_alive() and self.hero.is_alive():
                self.range_combat, self.hero_range_atk, self.monster_range_atk = self._select_range_and_atk()
                self.hero.attack(self.monster, self.range_combat, self.hero_range_atk)
                if self.monster.is_alive():
                    self.monster.attack(self.hero, self.range_combat, self.monster_range_atk)
                if len(self.hero.combat_range) == 1:
                    press_to_continue()

            if not self.hero.is_alive():
                box_msg("Too bad you are dead!")
            else:
                keep_going = ask_continue()
                self.hero.hp = self.hero.full_hp
                print("You heal yourself and venture further into the tunnel until you encounter:\n")

        if self.hero.is_alive():
            box_msg("Congratulation, you retired!")

        if ask_continue("Do you want to start over?"):
            self.restart()

    def _select_hero(self) -> Hero:
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
        chosen_monster = choice([k for k in self.monster_selector.keys()])
        monster_type: Archetype = self.monster_selector[chosen_monster]
        self.monster = Monster(monster_type.name, monster_type, self.hero.level)
        self.monster.print()

    def _select_hero_range(self, string: str) -> str:
        if len(self.hero.combat_range) == 1:
            return self.hero.combat_range[0]
        answer_choices: dict = generate_answer_selector(self.hero.combat_range)
        answer_description: list = generate_answer_selector_description(self.hero.combat_range)

        return ask_selection(string, answer_choices, answer_description)

    def _select_monster_range(self) -> str:
        if len(self.monster.combat_range) == 1:
            return self.monster.combat_range[0]

        return choice(self.monster.combat_range)

    def _select_range_and_atk(self) -> map:
        hero_range: str = self._select_hero_range("\nAt what RANGE do you want to attack?")
        hero_atk: str = self._select_hero_range("\nWhat KIND of attack do you want to perform?")
        monster_range: str = self._select_monster_range()
        monster_atk: str = self._select_monster_range()
        combat_range: str = hero_range
        if hero_range != monster_range:
            combat_range = choice([hero_range, monster_range])
        print(f"\nThe round range is {combat_range}, you will be performing a {hero_atk} and the {self.monster.name} "
              f"a {monster_atk} attack.")
        return map(lambda x: x == "range", [combat_range, hero_atk, monster_atk])

