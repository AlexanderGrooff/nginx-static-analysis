from argparse import ArgumentParser


def get_args():
    parser = ArgumentParser()
    parser.add_argument("directive", help="Parse directive from configs")
    parser.add_argument(
        "-f", "--file", help="Root nginx file", default="/etc/nginx/nginx.conf"
    )
    parser.add_argument(
        "-v", "--verbose", help="Set verbosity level to debug", action="store_true"
    )
    return parser.parse_args()
