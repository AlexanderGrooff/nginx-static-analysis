import sys
from argparse import SUPPRESS, ArgumentParser, FileType
from io import TextIOWrapper
from typing import Iterator, List, Optional, Union

from loguru import logger


def setup_logger(verbose: bool):
    log_level = "DEBUG" if verbose else "INFO"
    logger.remove()
    logger.add(sys.stderr, level=log_level, format="{message}")


def get_args(args: Optional[List[str]] = None):
    parser = ArgumentParser(prog="nginx-static-analysis")
    parser.add_argument(
        "--file", help="Root nginx file", default="/etc/nginx/nginx.conf"
    )
    parser.add_argument(
        "-v", "--verbose", help="Set verbosity level to debug", action="store_true"
    )
    parser.add_argument(
        "-q",
        "--quiet",
        help="Only show values. Useful for scripting",
        action="store_true",
    )
    parser.add_argument(
        "-f",
        "--filter",
        dest="filters",
        help="Filter values. Takes input as x=y, where x is the directive and y is the target value",
        action="append",
        default=[],
    )
    parser.add_argument(
        "-d",
        "--directive",
        dest="directives",
        help="Filter directive. If none given, show all found directives",
        action="append",
        default=[],
    )

    # Stdin logs
    parser.add_argument(
        "logs", nargs="*", default=sys.stdin, type=FileType("r"), help=SUPPRESS
    )
    return parser.parse_args(args=args)


def get_loglines(log_input: Union[List[TextIOWrapper], TextIOWrapper]) -> Iterator[str]:
    if isinstance(log_input, list):
        # Arg is given, not stdin
        for f in log_input:
            for l in f.buffer.readlines():
                yield l.decode("utf-8", errors="ignore")
    else:
        while not log_input.isatty():
            content = log_input.buffer.readline()
            if not content:
                break
            line = content.decode("utf-8", errors="ignore")
            yield line
