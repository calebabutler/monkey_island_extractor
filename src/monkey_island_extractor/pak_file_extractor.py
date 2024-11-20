#!/usr/bin/env python3
from dataclasses import dataclass
import io
import typing
import struct
import os

# Types

@dataclass
class FileToExtract:
    source: str
    destination: str

@dataclass
class Config:
    game_path: str
    pak_file_name: str
    files_to_extract: list[FileToExtract]

@dataclass
class Header:
    magic: int
    version: float
    start_of_index: int
    start_of_file_entries: int
    start_of_file_names: int
    start_of_data: int
    size_of_index: int
    size_of_file_entries: int
    size_of_file_names: int
    size_of_data: int

@dataclass
class FileEntry:
    file_data_pos: int
    file_name_pos: int
    data_size: int
    data_size2: int
    compressed: int

# Constants

default_path_table = {
    'Windows' : 'C:\\Program Files (x86)\\Steam\\steamapps\\common\\Monkey2',
    'Linux' : '~/.local/share/Steam/steamapps/common/The Secret of Monkey Island Special Edition',
}

# Functions

def read_header(pak_file: io.BufferedReader) -> Header:
    packed_header = pak_file.read(40)
    unpacked_header = struct.unpack('<IfIIIIIIII', packed_header)
    return Header(
        unpacked_header[0],
        unpacked_header[1],
        unpacked_header[2],
        unpacked_header[3],
        unpacked_header[4],
        unpacked_header[5],
        unpacked_header[6],
        unpacked_header[7],
        unpacked_header[8],
        unpacked_header[9],
    )


def read_file_entries(header: Header, pak_file: io.BufferedReader) -> list[FileEntry]:
    number_of_file_entries = header.size_of_file_entries // 20
    pak_file.seek(header.start_of_file_entries, os.SEEK_SET)
    file_entries = []
    for i in range(number_of_file_entries):
        packed_file_entry = pak_file.read(20)
        unpacked_file_entry = struct.unpack('<IIIII', packed_file_entry)
        file_entries.append(FileEntry(
            unpacked_file_entry[0],
            unpacked_file_entry[1],
            unpacked_file_entry[2],
            unpacked_file_entry[3],
            unpacked_file_entry[4],
        ))
    return file_entries


def read_file_names(file_entries: list[FileEntry], header: Header, pak_file: io.BufferedReader) -> list[str]:
    file_names = []
    pak_file.seek(header.start_of_file_names, os.SEEK_SET)
    for entry in file_entries:
        file_name_buffer = bytearray()
        while (byte := pak_file.read(1)) != bytearray([0]):
            file_name_buffer += byte
        file_names.append(file_name_buffer.decode())
    return file_names


def extract_file(source_file: str, destination_file: str, file_entries: list[FileEntry], file_names: list[str], header: Header, pak_file: io.BufferedReader) -> typing.NoReturn:
    source_file_index = file_names.index(source_file)
    pak_file.seek(header.start_of_data + file_entries[source_file_index].file_data_pos, os.SEEK_SET)
    with open(destination_file, 'wb') as extracted_file:
        extracted_file.write(pak_file.read(file_entries[source_file_index].data_size))


def run(config: Config) -> typing.NoReturn:
    with open(os.path.join(config.game_path, config.pak_file_name), 'rb') as pak_file:
        header = read_header(pak_file)
        file_entries = read_file_entries(header, pak_file)
        file_names = read_file_names(file_entries, header, pak_file)
        for file in config.files_to_extract:
            extract_file(file.source, file.destination, file_entries, file_names, header, pak_file)

