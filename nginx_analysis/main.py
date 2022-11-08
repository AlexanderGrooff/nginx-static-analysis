#!/usr/bin/env python

from loguru import logger

from nginx_analysis.analysis import (
    filter_config,
    get_directive_matches,
    get_unique_directives,
    parse_config,
)
from nginx_analysis.dataclasses import AnyFilter
from nginx_analysis.filter import args_to_filter, logline_to_filter
from nginx_analysis.input import get_args, get_loglines, setup_logger
from nginx_analysis.log import parse_logline
from nginx_analysis.output import render_directive_matches


def main():
    args = get_args()
    setup_logger(args.verbose)

    root_config = parse_config(args.file)
    search_directives = args.directives
    filters = args_to_filter(args.filters)
    if "logs" in args:
        # We combine all logline filters into an AnyFilter
        # to match directives that match any of the loglines
        logline_filters = []
        for line in get_loglines(args.logs):
            parsed_line = parse_logline(root_config, line)
            logger.debug(parsed_line)
            log_filter = logline_to_filter(parsed_line)
            logline_filters.append(log_filter)
        if logline_filters:
            filters += AnyFilter(filters=logline_filters)

    all_directives = get_unique_directives(root_config)
    logger.debug(f"Found directives in config: {all_directives}")

    filtered_lines = filter_config(root_config, filters)
    logger.debug(f"Found {len(filtered_lines)} lines matching filters")
    if search_directives:
        matching_lines = get_directive_matches(filtered_lines, search_directives)
    else:
        matching_lines = filtered_lines

    if matching_lines:
        logger.debug(f"Found the following values:")
        render_directive_matches(matching_lines)
    else:
        logger.info(f"Found no matches")


if __name__ == "__main__":
    main()
