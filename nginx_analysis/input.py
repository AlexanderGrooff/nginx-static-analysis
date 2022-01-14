from argparse import ArgumentParser


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
    directive_parser.add_argument("directive", help="Specify directive to look for")

    url_parser = subparsers.add_parser(
        "url", help="Find all configs that are hit when making a request"
    )
    url_parser.add_argument("url", help="Url to simulate request for")
    url_parser.add_argument(
        "-H", "--headers", help="Header in the request. Can be used multiple times"
    )
    return parser.parse_args()
