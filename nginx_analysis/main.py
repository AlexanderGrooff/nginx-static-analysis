#!/usr/bin/env python

from loguru import logger

from nginx_analysis.analysis import (
    get_directive_matches,
    get_unique_directives,
    parse_config,
)
from nginx_analysis.dataclasses import AllFilter
from nginx_analysis.filter import args_to_filter, logline_to_filters
from nginx_analysis.input import get_args, get_loglines, setup_logger
from nginx_analysis.log import parse_logline
from nginx_analysis.output import render_directive_matches
from nginx_analysis.url import get_server_configs_for_url


def main():
    args = get_args()
    setup_logger(args.verbose)

    root_config = parse_config(args.file)
    filters = AllFilter()
    if "logs" in args:
        for line in get_loglines(args.logs):
            parsed_line = parse_logline(root_config, line)
            logger.debug(parsed_line)
            log_filters = logline_to_filters(parsed_line)
            filters += log_filters

    if "directives" in args:
        directives = get_unique_directives(root_config)
        logger.debug(f"Found directives in config: {directives}")
        arg_filters = args_to_filter(args.directives, args.values)
        filters += arg_filters

        directive_matches = get_directive_matches(root_config, filters)
        if directive_matches:
            logger.debug(f"Found the following values:")
            render_directive_matches(directive_matches)
        else:
            logger.info(f"Found no matches")

    if "url" in args:
        server_configs = get_server_configs_for_url(args.url, root_config)
        if server_configs:
            for s in server_configs:
                logger.info(f"{s.file}:{s.line}")
        else:
            logger.info(f"Url {args.url} doesn't match any configs")


if __name__ == "__main__":
    main()
