#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""A beautifier for Bash shell scripts written in Python."""

import argparse
# import bashlex
import os
import pkg_resources
import sys

class Beautysh:
    """Class representing the beautifier and its associated methods"""

    def __init__(self):
        self.indent_char = ' '
        self.indent_length = 4
        self.backup = False
        self.check = False
        self.fix_function_style = False

    @property
    def version(self) -> str:
        try:
            return pkg_resources.require("beautysh")[0].version
        except pkg_resources.DistributionNotFound:
            return "not available"

    def read_file(self, path: 'os.PathLike[str]') -> str:
        """"Read text from a file"""
        with open(path, 'r') as f:
            return f.read()

    def write_file(self, path: 'os.PathLike[str]', data: str):
        """Write text to a file"""
        with open(path, 'w') as f:
            f.write(data)

    def parse_args(self):
        parser = argparse.ArgumentParser(
            description="A Bash beautifier for the masses, version {}"
                        .format(self.version),
            add_help=False)
        parser.add_argument('--indent_length',
                            '-i',
                            nargs=1,
                            type=int,
                            default=4,
                            help="Sets the number of spaces to be used in "
                                 "indentation.")
        parser.add_argument('--files',
                            '-f',
                            nargs='*',
                            help="Files to be beautified. This is mandatory. "
                            "If - is provided as filename, then beautysh reads"
                            " from stdin and writes on stdout.")
        parser.add_argument('--backup',
                            '-b',
                            action='store_true',
                            help="Beautysh will create a backup file in the "
                                 "same path as the original.")
        parser.add_argument('--check',
                            '-c',
                            action='store_true',
                            help="Beautysh will just check the files without "
                            "doing any in-place beautify.")
        parser.add_argument('--tab',
                            '-t',
                            action='store_true',
                            help="Sets indentation to tabs instead of spaces.")
        parser.add_argument('--fix_function_style',
                            '-s',
                            nargs=1,
                            type=str,
                            choices={"fnpar", "fnonly", "paronly"},
                            help="Force a specific Bash function formatting. "
                            "See below for more info.")
        parser.add_argument('--version',
                            '-v',
                            action='store_true',
                            help="Prints the version and exits.")
        parser.parse_args(namespace=self)
        if (len(sys.argv) < 2) or self.help:
            parser.print_help()
            exit()
        if self.version:
            print(self.version)
            exit()
        if not self.files:
            print("Please provide at least one input file")
            parser.print_help()
            exit()
        if self.tab:
            self.indent_length = 1
            self.indent_char = '\t'

    def cli(self):
        """Beautysh CLI mode"""
        self.parse_args()


if(__name__ == '__main__'):
    Beautysh().main()
