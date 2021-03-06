#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Various prompt functions

- prompt_question
- ask_continue
- ask_selection

"""
from DistUtils import warning_msg


def prompt_question(msg: str, answer_list: dict, separator: str = None):
    """Prompt a question with possible answer being the first character of the key of a dictionary and return the
    corresponding element."""
    possible_answer: list[str] = [k for k in answer_list.keys()]
    prompt_msg: str = msg + "\n"
    if separator:
        prompt_msg += f"{separator}".join(possible_answer) + ": "
    answer = input(prompt_msg).upper()
    while answer not in answer_list:
        print(warning_msg("Your selection is not in the list!"))
        answer = input(prompt_msg).upper()
    return answer_list[answer]


def ask_yes_no(msg: str) -> bool:
    """Prompt a simple yes/no question."""
    return prompt_question(msg, {"Y": True, "N": False}, " \\ ")


def ask_continue() -> bool:
    """Prompt a frequent yes/no question with predetermined message."""
    return ask_yes_no("Do you want to continue?")


def ask_selection(msg: str, answer_list: dict, answer_description: str):
    """Prompt a question, but a description of the answer choices is provided."""
    return prompt_question(msg + "\n" + answer_description, answer_list)


def press_to_continue() -> None:
    """Helper function to create a stop in the console."""
    input("\nPress ENTER to continue.\n")
