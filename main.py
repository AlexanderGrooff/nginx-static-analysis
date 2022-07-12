#!/usr/bin/env python

from loguru import logger

from nginx_analysis.analysis import (
    get_directive_matches,
    get_unique_directives,
    parse_config,
)
from nginx_analysis.input import get_args, setup_logger
from nginx_analysis.log import parse_logline
from nginx_analysis.output import render_directive_matches
from nginx_analysis.url import get_server_configs_for_url


def main():
    args = get_args()
    setup_logger(args.verbose)

    root_config = parse_config(args.file)
    if "directive" in args:
        directives = get_unique_directives(root_config)
        logger.debug(f"Found directives in config: {directives}")
        directive_matches = get_directive_matches(root_config, args.directive)
        if directive_matches:
            logger.debug(f"Found the following {args.directive} values:")
            render_directive_matches(directive_matches)
        else:
            logger.info(f"Found no matches for directive {args.directive}")
    if "url" in args:
        server_configs = get_server_configs_for_url(args.url, root_config)
        if server_configs:
            for s in server_configs:
                logger.info(f"{s.file}:{s.line}")
        else:
            logger.info(f"Url {args.url} doesn't match any configs")
    if "logs" in args:
        log_lines = []
        if isinstance(args.logs, list):
            # Arg is given, not stdin
            for f in args.logs:
                log_lines.extend(f.readlines())
        else:
            # TODO: fix tail -f
            for line in args.logs.buffer.raw.readlines():
                log_lines.append(line.decode("utf-8", errors="ignore"))

        for line in log_lines:
            parsed_line = parse_logline(root_config, line)
            logger.info(parsed_line)


if __name__ == "__main__":
    main()
