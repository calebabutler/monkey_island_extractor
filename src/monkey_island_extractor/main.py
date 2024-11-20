#!/usr/bin/env python3
import sys
import platform
import typing
import os
from monkey_island_extractor import pak_file_extractor
from beaupy import confirm, prompt, select, select_multiple
from beaupy.spinners import *
from rich.console import Console

# Globals

default_path_table_for_monkey_island1 = {
    'Windows' : 'C:\\Program Files (x86)\\Steam\\steamapps\\common\\The Secret of Monkey Island Special Edition',
    'Linux' : '~/.local/share/Steam/steamapps/common/The Secret of Monkey Island Special Edition'
}

default_path_table_for_monkey_island2 = {
    'Windows' : 'C:\\Program Files (x86)\\Steam\\steamapps\\common\\Monkey2',
    'Linux' : '~/.local/share/Steam/steamapps/common/Monkey2'
}

# Functions


def get_game_path(args: list[str], default_path_table: dict[str, str]) -> str:
    if len(args) > 1:
        path = args[1]
    else:
        try:
            path = default_path_table[platform.system()]
        except ValueError:
            path = False
    while path == False or not os.path.exists(path):
        path = prompt('Cannot find game path. Where is the game?', target_type=str)
    return path


def extract_monkey_island1(args: list[str]) -> typing.NoReturn:
    game_path = get_game_path(args, default_path_table_for_monkey_island1)
    pak_file_extractor.run(pak_file_extractor.Config(
        game_path=game_path,
        pak_file_name='Monkey1.pak',
        files_to_extract=[
            pak_file_extractor.FileToExtract(
                source='classic/en/monkey1.000',
                destination='MONKEY1.000',
            ),
            pak_file_extractor.FileToExtract(
                source='classic/en/monkey1.001',
                destination='MONKEY1.001',
            ),
        ],
    ))


def extract_monkey_island2(args: list[str]) -> typing.NoReturn:
    game_path = get_game_path(args, default_path_table_for_monkey_island2)
    pak_file_extractor.run(pak_file_extractor.Config(
        game_path=game_path,
        pak_file_name='monkey2.pak',
        files_to_extract=[
            pak_file_extractor.FileToExtract(
                source='classic/en/monkey2.000',
                destination='MONKEY2.000',
            ),
            pak_file_extractor.FileToExtract(
                source='classic/en/monkey2.001',
                destination='MONKEY2.001',
            ),
        ],
    ))

def main(args: list[str]) -> typing.NoReturn:
    games = [
        'The Secret of Monkey Island: Special Edition',
        'Monkey Island 2: Special Edition',
    ]
    console = Console()
    console.print('Which monkey island game would you like to extract?')
    game = select(games)
    [extract_monkey_island1, extract_monkey_island2][games.index(game)](args)


if __name__ == '__main__':
    main(sys.argv)
