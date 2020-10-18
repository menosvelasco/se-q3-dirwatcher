#!/usr/bin/env python3
"""
Dirwatcher - A long-running program
"""

__author__ = "Manuel velasco, John(Q3 Tutor) and Peter Mayor"

import sys
import signal
import logging
import os
import time
import argparse
from colorama import Fore


logging.basicConfig(format='%(asctime)s.%(msecs)03d %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S', level=logging.DEBUG)
logger = logging.getLogger(__name__)

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
    list_file = os.listdir(path)
    for k in list(global_dict):
        if k.split('/')[1] not in list_file:
            logger.info(f"file Deleted {k}")
            global_dict.pop(k)
    for _file in list_file:
        path_file = path + "/" + _file

        if path_file not in global_dict and path_file.endswith(extension):
            logger.info(f"adding new file {path_file}")
            global_dict[path_file] = 0

        if path_file.endswith(extension):
            search_for_magic(path_file, global_dict[path_file], magic_string)

    return


def create_parser():
    """create agr terminal"""
    parser = argparse.ArgumentParser(
        description="watch directory for file changes")
    parser.add_argument("-e", "--ext", help="extension input")
    parser.add_argument("-d", "--dir", help="directory input")
    parser.add_argument(
        "-i", "--int", default=1, help="this is the polling\
            how long we check the directory.")
    parser.add_argument(
        "-t", "--text", help="this is the magic string search",)

    return parser


def signal_handler(sig_num, frame):
    """Use Handling OS signals"""
    logger.warning('Received ' + signal.Signals(sig_num).name)
    if signal.Signals(sig_num).name == "SIGINT":
        logger.info('Terminating Dirwatcher')

    if signal.Signals(sig_num).name == "SIGTERM":
        logger.info('Terminating Dirwatcher os interupt recieved')

    global exit_flag
    exit_flag = True

    return


def main(args):
    ns = create_parser().parse_args()
    # Hook into these two signals from the OS
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    # Now my signal_handler will get called if OS sends
    # either of these to my process.
    print(Fore.GREEN+"#############################################################################")
    print()
    logging.info("Starting program dirwatcher.py")
    print()
    print("#############################################################################")
    while not exit_flag:
        try:
            watch_directory(ns.dir, ns.text, ns.ext, ns.int)
            pass
        except Exception as e:
            # This is an UNHANDLED exception
            # Log an ERROR level message here
            logger.error(e)
            pass
    print(Fore.RED+"_______________________________________________________________________________")
    print()
    logging.info("GoodBye Stopped dirwatcher.py")
    print()
    print("_______________________________________________________________________________")
    # put a sleep inside my while loop so I don't peg the cpu usage at 100%
    time.sleep(ns.int)

    # final exit point happens here
    # Log a message that we are shutting down
    # Include the overall uptime since program start
    # search_for_magic("hello.txt", 0, ns.text)
    print(ns)
    return


if __name__ == '__main__':
    main(sys.argv[1:])
