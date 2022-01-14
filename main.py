#!/usr/bin/env python

from loguru import logger

from nginx_analysis.analysis import (
    get_directive_matches,
    get_unique_directives,
    parse_config,
)
from nginx_analysis.input import get_args
from nginx_analysis.log import setup_logger
from nginx_analysis.output import render_directive_matches
from nginx_analysis.url import get_server_config_for_url

if __name__ == "__main__":
    args = get_args()
    setup_logger(args.verbose)

    root_config = parse_config(args.file)
    if "directive" in args:
        directives = get_unique_directives(root_config)
        logger.debug(f"Found directives in config: {directives}")
        directive_matches = get_directive_matches(root_config, args.directive)
        if directive_matches:
            logger.info(f"Found the following {args.directive} values:")
            render_directive_matches(directive_matches)
        else:
            logger.info(f"Found no matches for directive {args.directive}")
    if "url" in args:
        server_config = get_server_config_for_url(args.url, root_config)
        if server_config:
            logger.info(
                f"Found URL in serverblock {server_config.file}:{server_config.line}"
            )
        else:
            logger.info(f"Url {args.url} doesn't match any config")
