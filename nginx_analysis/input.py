from argparse import ArgumentParser
from nginx_analysis.analysis import get_unique_directives



def get_args():
    parser = ArgumentParser()
    parser.add_argument("directive", help="Parse directive from configs")
    parser.add_argument("-f", "--file", help="Root nginx file", default="/etc/nginx/nginx.conf")
    return parser.parse_args()