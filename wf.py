"""Command line utility for running external programs on file changes."""
from typing import Final
from time import sleep
import argparse
import enum
import os
import logging
import sys
import subprocess


@enum.unique
class Loglevels(enum.IntEnum):
    """Logging levels."""

    NOTSET, DEBUG, INFO, WARNING, ERROR, CRITICAL = range(6)


def generate_argparser(prog: str) -> argparse.ArgumentParser:
    """Generate an ArgumentParser object for this script."""
    PARSER = argparse.ArgumentParser(prog=prog, usage="Watches files for changes")

    PARSER.add_argument(
        'files',
        nargs="*",
    )

    PARSER.add_argument(
        '-t', '--time',
        default=10,
        type=int,
        help="Wait time between executions"
    )

    PARSER.add_argument(
        '-s', '--shell',
        type=str,
        help="Program that will be run after the wait time has passed.\n Please specify it through a single string."
    )

    PARSER.add_argument(
        '-v', '--verbosity',
        type=str,
        default="INFO",
        help="Application's verbosity level"
    )

    return PARSER


def main() -> int:
    """Set up everything and run the external commands."""
    ARGUMENTS: Final[argparse.Namespace] = generate_argparser('wf').parse_args()

    if ARGUMENTS.verbosity.upper() not in Loglevels.__dict__:
        ARGUMENTS.verbosity = "CRITICAL"

    logging.basicConfig(
        format="[%(levelname)s] %(message)s",
        level=(Loglevels[ARGUMENTS.verbosity] * 10),
        force=True,
        stream=sys.stderr
    )

    if not ARGUMENTS.files:
        logging.critical("No file specified for the program.")
        return 1

    if not ARGUMENTS.shell:
        logging.critical("No program specified through --shell argument.")
        return 1

    PROGRAM_LIST: list[str] = ARGUMENTS.shell.split(" ")

    file_mtime = {x: os.path.getmtime(x) for x in ARGUMENTS.files}

    try:
        while True:
            logging.debug(f"Sleeping for {ARGUMENTS.time} seconds")
            sleep(ARGUMENTS.time)
            for FILE in ARGUMENTS.files:
                if (CURRENT_MTIME := os.path.getmtime(FILE)) == file_mtime[FILE]:
                    logging.debug(f"[{FILE}] No file changes since last check")
                    continue
                logging.info(f"[{FILE}] File change detected. Running {PROGRAM_LIST}")
                subprocess.run(PROGRAM_LIST)
                file_mtime[FILE] = CURRENT_MTIME
    except KeyboardInterrupt:
        logging.critical("Program successfully exited through KeyboardInterrupt")

    return 0


if __name__ == "main":
    raise SystemExit(main())
