from typing import List, Set

import crossplane
from loguru import logger

from nginx_analysis.dataclasses import NginxLineConfig, RootNginxConfig


def parse_config(file_path: str) -> RootNginxConfig:
    """
    Extract and parse the Nginx config from the given file.
    """
    parsed_config = crossplane.parse(file_path)
    root_config = RootNginxConfig(**parsed_config)
    return root_config


def get_unique_directives_in_line(line_config: NginxLineConfig) -> Set[str]:
    """
    Loop recursively over the line and find unique directives
    """
    logger.debug(f"Parsing lineconfig {line_config}")
    directives = set()
    directives.add(line_config.directive)
    if line_config.block:
        for block_config in line_config.block:
            directives_in_block = get_unique_directives_in_line(block_config)
            directives = directives.union(list(directives_in_block))

    return directives


def get_unique_directives(root_config: RootNginxConfig) -> List[str]:
    """
    Find all unique directives in the given root config
    """
    unique_directives: Set[str] = set()
    for file_config in root_config.config:
        for line_config in file_config.parsed:
            directives = get_unique_directives_in_line(line_config)
            logger.debug(
                f"Found directives on line {line_config.line} in file {file_config.file}: {directives}"
            )
            unique_directives = unique_directives.union(directives)
    return list(unique_directives)


def get_directive_values_from_line(
    directive_name: str, line_config: NginxLineConfig
) -> List[str]:
    """
    Find all values for the given directive name in the line config, and go over blocks recursively
    """
    values = []
    if line_config.directive == directive_name:
        values += line_config.args

    if line_config.block:
        for block_config in line_config.block:
            values += get_directive_values_from_line(directive_name, block_config)
    return values


def get_directive_values(
    root_config: RootNginxConfig, directive_name: str
) -> List[str]:
    """
    Find all values for the given directive name in the root config
    """
    values = []
    for file_config in root_config.config:
        for line_config in file_config.parsed:
            line_values = get_directive_values_from_line(directive_name, line_config)
            logger.debug(
                f"Found directive values on line {line_config.line} in file {file_config.file}: {line_values}"
            )
            values += line_values
    return values
