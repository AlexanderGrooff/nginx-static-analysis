#!/usr/bin/env python
import sys

from loguru import logger

from nginx_analysis.analysis import (
    get_directive_values,
    get_unique_directives,
    parse_config,
)
from nginx_analysis.input import get_args

if __name__ == "__main__":
    args = get_args()

    log_level = "DEBUG" if args.verbose else "INFO"
    logger.remove()
    logger.add(sys.stderr, level=log_level)

    root_config = parse_config(args.file)
    directives = get_unique_directives(root_config)
    logger.info(f"Found directives in config: {directives}")
    directive_values = get_directive_values(root_config, args.directive)
    logger.info(f"Found the following {args.directive} values: {directive_values}")
