from typing import Iterator, List, Optional, Set, Tuple

import crossplane
from loguru import logger

from nginx_analysis.dataclasses import (
    DirectiveFilter,
    NginxLineConfig,
    RootNginxConfig,
    filter_unique,
    get_children_recursive,
    get_parents_recursive,
)


def sort_by_depth(line_configs: List[NginxLineConfig]) -> List[NginxLineConfig]:
    """
    Sort by nr of parents, then alphabetically on filename and then by line number.
    """
    return sorted(
        line_configs,
        key=lambda line_config: (
            len(get_parents_recursive(line_config)),
            line_config.file,
            line_config.line,
        ),
    )


def nginx_to_regex(nginx: str) -> str:
    """
    Convert a nginx-style regex to a python regex.
    Wildcard files are converted to regexes that match any file in the directory.
    """
    return nginx.replace("*", r"[^/]*")


def set_parents_in_include(root_config: RootNginxConfig, block_config: NginxLineConfig):
    if block_config.directive == "include":
        for file_path in block_config.args:
            nested_file_configs = root_config.get_files(nginx_to_regex(file_path))
            for nested_file_config in nested_file_configs:
                for nested_line_config in nested_file_config.parsed:
                    nested_line_config.parent = block_config
                    block_config.children.append(nested_line_config)
                    set_parents_in_include(root_config, nested_line_config)


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
    for line_config in root_config.lines:
        directives = get_unique_directives_in_line(line_config)
        logger.debug(
            f"Found directives on line {line_config.line} in file {line_config.file}: {directives}"
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


def is_partial_direct_match(
    line: NginxLineConfig, filters: List[DirectiveFilter]
) -> Optional[DirectiveFilter]:
    """
    Check if the line matches any of the filters. If it does, return the
    filter. If it doesn't, return None."""
    for dfilter in filters:
        if dfilter.match(line):
            logger.debug(f"Direct match on filter {dfilter}: {line}")
            return dfilter
    return None


def get_matching_lines_in_children(
    line: NginxLineConfig, filters: List[DirectiveFilter]
) -> Tuple[List[NginxLineConfig], List[DirectiveFilter]]:
    """
    Check if the line matches filters. If it matches, return the line.
    If it doesn't match, check if any of the children match the filters.
    We also return a list of filters that matched, so we can check if
    all filters were matched eventually.
    If there are no matches, return an empty list for both the matching
    lines and the matched filters.
    """
    if not filters:
        # No filters, meaning that the line matches directly
        return [line], []

    logger.debug(f"Checking if line {line} matches filters: {filters}")
    matched_filter = is_partial_direct_match(line, filters)
    if matched_filter:
        logger.debug(f"Found match in children: {line}")
        all_matched_filters = set([matched_filter])
        # Search for remaining filters in children, as the parent
        # might still be looking for other filters
        for child in line.children:
            remaining_filters = [f for f in filters if f not in all_matched_filters]
            if remaining_filters:
                logger.debug(
                    f"Looking for remaining filters in child {child}: {remaining_filters}"
                )
                _, child_matched_filters = get_matching_lines_in_children(
                    child, remaining_filters
                )
                all_matched_filters.update(child_matched_filters)
            else:
                logger.debug(
                    f"Found all filters in children of line {line}. We should stop!"
                )
                break
        return [line], list(all_matched_filters)

    # All filters must match at least one child
    matched_filters = set()
    matches = []
    for child in line.children:
        remaining_filters = [f for f in filters if f not in matched_filters]
        if remaining_filters:
            child_matches, child_matched_filters = get_matching_lines_in_children(
                child, remaining_filters
            )
            if child_matches:
                matches.extend(child_matches)
                matched_filters.update(child_matched_filters)
        else:
            logger.debug(
                f"Found all filters in children of line {line}. We should stop!"
            )
            break

    if len(matched_filters) == len(filters):
        logger.debug(
            f"Matched all ({len(matched_filters)}) filters in children: {line}"
        )
        return matches, list(matched_filters)
    return [], []


def expand_upon_direct_match(
    match: NginxLineConfig, matched_filters: List[DirectiveFilter]
) -> List[NginxLineConfig]:
    """
    Expand upon matching lines by recursively looking through
    parents and neighbours. However, we don't want to include any
    lines that have the same directive as in the filters.
    F.e., if the filter looks for location=/banaan, we don't want
    to include other recursive location lines.
    """
    matching_lines = []
    for neighbour in match.neighbours:
        matching_lines.append(neighbour)
        matching_lines.extend(get_children_recursive(neighbour))
    parents = get_parents_recursive(match)
    matching_lines.extend(parents)
    return matching_lines


def filter_config(
    lines: List[NginxLineConfig],
    filters: List[DirectiveFilter],
) -> List[NginxLineConfig]:
    """
    Find all values for the given directive name in the root config
    """
    if not filters:
        return sort_by_depth(filter_unique(lines))

    matching_lines = []
    for line in lines:
        child_matches, _ = get_matching_lines_in_children(line, filters)
        matching_lines.extend(child_matches)
        for match in child_matches:
            matching_lines.extend(expand_upon_direct_match(match, filters))

    return sort_by_depth(filter_unique(matching_lines))


def get_directive_matches(
    lines: Iterator[NginxLineConfig], directives: List[str]
) -> List[NginxLineConfig]:
    """
    Find all lines that match one of the given directives
    """
    return [line for line in lines if line.directive in directives]
