import sys
from argparse import ArgumentParser, FileType
from io import TextIOWrapper
from typing import Iterator, List, Union

from loguru import logger


def setup_logger(verbose: bool):
    log_level = "DEBUG" if verbose else "INFO"
    logger.remove()
    logger.add(sys.stderr, level=log_level, format="{message}")


def get_args():
    parser = ArgumentParser(prog="nginx-static-analysis")
    parser.add_argument(
        "-f", "--file", help="Root nginx file", default="/etc/nginx/nginx.conf"
    )
    parser.add_argument(
        "-v", "--verbose", help="Set verbosity level to debug", action="store_true"
    )
    subparsers = parser.add_subparsers(help="Commands available to run", required=True)

    directive_parser = subparsers.add_parser(
        "directive", help="Parse directive from configs"
    )
    directive_parser.add_argument(
        "directives", nargs="+", help="Specify directives to look for"
    )
    directive_parser.add_argument(
        "--value", nargs="*", help="Specify values to look for", default=[]
    )

    url_parser = subparsers.add_parser(
        "url", help="Find all configs that are hit when making a request"
    )
    url_parser.add_argument("url", help="Url to simulate request for")
    url_parser.add_argument(
        "-H", "--headers", help="Header in the request. Can be used multiple times"
    )

    log_parser = subparsers.add_parser(
        "log", help="Parse Nginx logs from stdin or given files"
    )
    log_parser.add_argument(
        "logs",
        nargs="*",
        default=sys.stdin,
        type=FileType("r"),
        help="Log file(s) to parse or stdin",
    )
    return parser.parse_args()


def get_loglines(log_input: Union[List[TextIOWrapper], TextIOWrapper]) -> Iterator[str]:
    if isinstance(log_input, list):
        # Arg is given, not stdin
        for f in log_input:
            for l in f.buffer.readlines():
                yield l.decode("utf-8", errors="ignore")
    else:
        while True:
            content = log_input.buffer.readline()
            if not content:
                break
            line = content.decode("utf-8", errors="ignore")
            yield line
