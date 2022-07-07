#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Various prompt functions

- prompt_question
- ask_continue
- ask_selection

"""
from DistUtils.print_utils import warning_msg

ask_yes_no_answer = {"Y": True, "N": False}


def prompt_question(msg: str, answer_list: dict, separator: str = None):
    possible_answer: list[str] = [k for k in answer_list.keys()]
    prompt_msg: str = msg + "\n"
    if separator:
        prompt_msg += f"{separator}".join(possible_answer) + ": "
    answer = input(prompt_msg).upper()
    while answer not in answer_list:
        print(warning_msg("Your selection is not in the list!"))
        answer = input(prompt_msg).upper()
    return answer_list[answer]


def ask_continue(msg: str = "Do you want to continue?") -> bool:
    return prompt_question(msg, ask_yes_no_answer, " \\ ")


def ask_selection(msg: str, answer_list: dict, answer_description: str):
    return prompt_question(msg + "\n" + answer_description, answer_list)


def press_to_continue() -> None:
    input("\nPress ENTER to continue.\n")
