#!/usr/bin/env python
# -*- coding: utf-8 -*-

# from classes import Game

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # Game.start()
    from Models.archetypes import rooster

    print(rooster)
    print(rooster.heroes)
    heroes = rooster.heroes
    for hero in heroes:
        hero.print()
    monsters = rooster.monsters
    for monster in monsters:
        monster.print()


