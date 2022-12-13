"""Command line utility for running external programs on file changes."""
from typing import Union, Mapping, Final
import sys
import subprocess
import argparse
from time import sleep
import os
import logging


def transform_verbosity(verbosity: Union[str, int]) -> int:
    """Transform logging verbosity levels from strings to valid integers."""
    LEVELS: Mapping[str, int] = {
        'NOTSET': 0, 'DEBUG': 10,
        'INFO': 20, 'WARNING': 30,
        'ERROR': 40, 'CRITICAL': 50
    }
    return LEVELS.get(verbosity, 50) if (type(verbosity) is str) else int(verbosity)


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
    ARGUMENTS = generate_argparser('wf').parse_args()

    if not ARGUMENTS.shell:
        print("No program specified through --shell argument. Exiting.", file=sys.stderr)
        return 1

    PROGRAM_LIST: list[str] = ARGUMENTS.shell.split(" ")
    VERBOSITY_LEVEL: Final[int] = transform_verbosity(ARGUMENTS.verbosity)
    FORMAT: Final[str] = "[%(levelname)s] %(message)s" if (VERBOSITY_LEVEL < logging.INFO) else "%(message)s"
    logging.basicConfig(format=FORMAT, level=VERBOSITY_LEVEL, force=True)
    logging.debug(f"Logging level set to {ARGUMENTS.verbosity:}: {VERBOSITY_LEVEL}")

    file_mtime = {x: os.path.getmtime(x) for x in ARGUMENTS.files}

    try:
        while True:
            logging.debug(f"Sleeping for {ARGUMENTS.time} seconds")
            sleep(ARGUMENTS.time)
            for FILE in ARGUMENTS.files:
                if (CURRENT_MTIME := os.path.getmtime(FILE)) == file_mtime[FILE]:
                    logging.info(f"[{FILE}] No file changes since last check")
                    continue
                logging.info(f"[{FILE}] File change detected. Running {PROGRAM_LIST}")
                subprocess.run(PROGRAM_LIST)
                file_mtime[FILE] = CURRENT_MTIME
    except KeyboardInterrupt:
        print("Program successfully exited through KeyboardInterrupt.", file=sys.stderr)
    return 0


if __name__ == "main":
    raise SystemExit(main())
