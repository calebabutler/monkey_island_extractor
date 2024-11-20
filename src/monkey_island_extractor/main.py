#!/usr/bin/env python3
import sys
import platform
import typing
from monkey_island_extractor import pak_file_extractor

default_path_table = {
    'Windows' : 'C:\\Program Files (x86)\\Steam\\steamapps\\common\\The Secret of Monkey Island Special Edition',
    'Linux' : '~/.local/share/Steam/steamapps/common/The Secret of Monkey Island Special Edition'
}


def main(args: list[str]) -> typing.NoReturn:
    if len(args) > 1:
        game_path = args[1]
    else:
        game_path = default_path_table[platform.system()]
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


if __name__ == '__main__':
    main(sys.argv)