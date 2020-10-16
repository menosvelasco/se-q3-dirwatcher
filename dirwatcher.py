#!/usr/bin/env python3
"""
Dirwatcher - A long-running program
"""

__author__ = "Manuel velasco"

import sys
import signal
import logging
import os
import time
import argparse


global_dict = {}
exit_flag = False


def search_for_magic(filename, start_line, magic_string):
    """magic string"""
    with open(filename) as f:
        file_f = f.readlines()
        line_find = []
        for line_num, line in enumerate(file_f):

            if line_num < start_line:
                continue

            global_dict[filename] = line_num + 1
            result = line.find(magic_string)

            if result != -1:
                line_find.append(line_num+1)
        if len(line_find) > 0:
            logger.info(f"new Magic-string {filename} line {line_find}")
        return


def watch_directory(path, magic_string, extension, interval):
    """directory create it. (os.makedirs) or (os.path.isdir)"""
    # Your code here
    return


def create_parser():
    """create agr terminal"""
    parser = argparse.ArgumentParser(
        description="watch directory for file changes")
    parser.add_argument("-e", "--ext", help="extension input")
    parser.add_argument("-d", "--dir", help="directory input")
    parser.add_argument("-i", "--int", default=1,
                        help="this is the polling how long we check the directory.")
    parser.add_argument(
        "-t", "--text", help="this is the magic string search",)

    return parser


def signal_handler(sig_num, frame):
    """Use Handling OS signals"""
    # Your code here
    return


def main(args):
    ns = create_parser().parse_args()
    search_for_magic("hello.txt", 0, ns.text)
    print(ns)
    return


if __name__ == '__main__':
    main(sys.argv[1:])
