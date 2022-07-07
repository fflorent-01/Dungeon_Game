#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Various printing functions

- warning_msg
- box_msg
"""


def warning_msg(msg: str, symbol: str = "*", repeat: int = 5) -> str:
    """
    Adds a decorator to a single line message.

    :param msg: Message you want to decorate
    :param symbol: Decorator character
    :param repeat: Number of repetition at beginning and end fo the string
    :return: Decorated string (*** msg ***)
    """
    decorator = symbol * repeat
    return "\n" + decorator + " " + msg + " " + decorator


def box_msg(msg: str, symbol: str = "#") -> str:
    """
    Creates a box around your message

    :param msg: Message you want in the box
    :param symbol: Decorator you want to use to create your box
    :return: Decorated string (box)
    """
    top = bottom = symbol * (len(msg) + 4)
    text = symbol + " " + msg + " " + symbol
    print("\n" + "\n".join([top, text, bottom]) + "\n")
