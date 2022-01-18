from dataclasses import dataclass, field
import heapq
from typing import Any


def get_name():
    return globals()["__file__"].split("\\")[-1].split(".")[0]


def read_input(num_day):
    fname = f"day{num_day}_input.txt"
    with open(fname) as f:
        out = f.read()
    return out
