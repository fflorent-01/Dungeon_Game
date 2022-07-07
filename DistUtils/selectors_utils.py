#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Various selector functions

- type_selector
- type_selection_description
"""
from Models.archetypes import Archetype


def type_selector(lst: list[Archetype]) -> dict[str, Archetype]:
    """
    Takes a rooster list and return a dict

    :param lst: rooster list
    :return: {"Archetype.name[0]" : Archetype, ...}
    """
    return {elem.name[0].upper(): elem for elem in lst}


def type_selection_description(lst: list[Archetype]) -> str:
    """
    Takes a rooster list and return a string that describes the selection

    :param lst: rooster list
    :return: Archetype.name[0]: Archetype.name \n ...
    """
    return "\n".join([elem.name[0].upper() + ": " + elem.name for elem in lst])


def generate_answer_selector(lst: list[str]) -> dict[str, str]:
    return {elem[0].upper(): elem for elem in lst}


def generate_answer_selector_description(lst: list[str]) -> str:
    return "\n".join([elem[0].upper() + ": " + elem for elem in lst])
