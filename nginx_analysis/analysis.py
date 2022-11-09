from typing import Iterator, List, Optional, Set, Tuple

import crossplane
from loguru import logger

from nginx_analysis.dataclasses import (
    DirectiveFilter,
    NginxLineConfig,
    RootNginxConfig,
    get_children_recursive,
)


def set_parents_in_include(root_config: RootNginxConfig, block_config: NginxLineConfig):
    if block_config.directive == "include":
        for file_path in block_config.args:
            nested_file_configs = root_config.get_files(file_path)
            for nested_file_config in nested_file_configs:
                for nested_line_config in nested_file_config.parsed:
                    nested_line_config.parent = block_config
                    block_config.children.append(nested_line_config)


def set_parents_of_blocks(root_config: RootNginxConfig, line_config: NginxLineConfig):
    if line_config.block:
        for block_config in line_config.block:
            block_config.parent = line_config
            line_config.children.append(block_config)
            block_config.file = line_config.file
            set_parents_of_blocks(root_config, block_config)
    set_parents_in_include(root_config, line_config)


def parse_config(file_path: str) -> RootNginxConfig:
    """
    Extract and parse the Nginx config from the given file.
    """
    parsed_config = crossplane.parse(file_path)
    root_config = RootNginxConfig(**parsed_config)

    # Add parent to all lines for backtracking
    for file_config in root_config.config:
        for line_config in file_config.parsed:
            line_config.file = file_config.file
            set_parents_of_blocks(root_config, line_config)
    return root_config


def get_unique_directives_in_line(line_config: NginxLineConfig) -> Set[str]:
    """
    Loop recursively over the line and find unique directives
    """
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


def get_line_at_linenr(
    root_config: RootNginxConfig, linenr: int
) -> Optional[NginxLineConfig]:
    for line in root_config.lines:
        if line.line == linenr:
            return line
    return None


def is_direct_match(
    line: NginxLineConfig, filters: List[DirectiveFilter]
) -> Optional[DirectiveFilter]:
    for dfilter in filters:
        if dfilter.match(line):
            logger.debug(f"Direct match: {line}")
            return dfilter
    return None


def find_matches_in_children(
    line: NginxLineConfig, filters: List[DirectiveFilter]
) -> Tuple[List[NginxLineConfig], List[DirectiveFilter]]:
    if matched_filter := is_direct_match(line, filters):
        all_matched_filters = set([matched_filter])
        # Search for remaining filters in children, as the parent
        # might still be looking for other filters
        remaining_filters = [f for f in filters if f != matched_filter]
        for child in line.children:
            _, child_matched_filters = find_matches_in_children(
                child, remaining_filters
            )
            all_matched_filters.update(child_matched_filters)
        return [line, *get_children_recursive(line)], list(all_matched_filters)

    # All filters must match at least one child
    matched_filters = set()
    matches = [line]
    for child in line.children:
        child_matches, child_matched_filters = find_matches_in_children(child, filters)
        if child_matches:
            matches.extend(child_matches)
            matched_filters.update(child_matched_filters)

    if len(matched_filters) == len(filters):
        logger.debug(
            f"Matched all ({len(matched_filters)}) filters in children: {line}"
        )
        return matches, list(matched_filters)
    return [], []


def filter_config(
    lines: Iterator[NginxLineConfig],
    filters: List[DirectiveFilter],
) -> List[NginxLineConfig]:
    """
    Find all values for the given directive name in the root config
    """
    matching_lines = []
    for line in lines:
        child_matches, _ = find_matches_in_children(line, filters)
        matching_lines.extend(child_matches)

    return matching_lines


def get_directive_matches(
    lines: List[NginxLineConfig], directives: List[str]
) -> List[NginxLineConfig]:
    """
    Find all lines that match one of the given directives
    """
    return [line for line in lines if line.directive in directives]
