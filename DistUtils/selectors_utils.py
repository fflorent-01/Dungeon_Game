#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Various selector functions

- type_selector
- type_selection_description
"""
from Models import Archetype


def create_selection_dict(lst: list[object], attr: str) -> dict[str, object]:
    """
    Takes a list of objet and return a dict containing first letter of attr and the object.

    :param lst: A list of object
    :param attr: An attribute name
    :return: {object.attr[0]: object, ...}
    """
    return {getattr(elem, attr)[0].upper(): elem for elem in lst}


def create_selection_description(lst: list[object], attr: str) -> str:
    """
    Takes a list of object and return a string that is line break delimited of first letter of attr and attr.

    :param lst: A list of object
    :param attr: An attribute name
    :return: object.attr[0]: object\n...
    """
    return "\n".join([getattr(elem, attr)[0].upper() + ": " + getattr(elem, attr) for elem in lst])


def generate_answer_selector(lst: list[str]) -> dict[str, str]:
    return {elem[0].upper(): elem for elem in lst}


def generate_answer_selector_description(lst: list[str]) -> str:
    return "\n".join([elem[0].upper() + ": " + elem for elem in lst])
