#!/usr/bin/env python3
from dataclasses import dataclass
import typing

# Types

@dataclass
class FilePair:
    file1: str
    file2: str

@dataclass
class Config:
    game_path: str
    xwb_file_name: str
    swap_file_pair: list[FilePair]

# Functions

def run(config: Config) -> typing.NoReturn:
    pass