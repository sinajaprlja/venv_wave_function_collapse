#! /usr/bin/python3

import config

import time

def verbose(message: str, level: int) -> None:
    if 0 <= level <= config.DEBUG_LEVEL:
        print(f"{timestring()} {message}")
    elif level < 0 or level > 3:
        raise ValueError(f"{level} is out of range [0, 3]")

def timestring() -> str:
    return time.strftime('[%H:%M:%S]', time.gmtime())
