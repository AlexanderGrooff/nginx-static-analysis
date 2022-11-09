import re
from typing import List

from loguru import logger

from nginx_analysis.analysis import filter_config
from nginx_analysis.dataclasses import DirectiveFilter, RootNginxConfig


def get_all_nginx_logformats(root_config: RootNginxConfig) -> List[str]:
    """
    Parse the logformat from the Nginx config.
    Defaults to the 'combined' logformat if none
    were found.
    """
    # TODO: Add default error log
    default = (
        "$remote_addr - $remote_user [$time_local] "
        '"$request" $status $body_bytes_sent '
        '"$http_referer" "$http_user_agent"'
    )
    # TODO: Only match logformat for matching logfile
    log_format_lines = filter_config(
        root_config, [DirectiveFilter(directive="log_format")]
    )
    if not log_format_lines:
        return [default]

    parsed_logformats = []
    for line_config in log_format_lines:
        # TODO: Parse JSON nicely
        if line_config.args[1].startswith("escape="):
            logformat = "".join(line_config.args[2:])
        else:
            logformat = "".join(line_config.args[1:])
        logger.debug(f"Found logformat: {logformat}")
        parsed_logformats.append(logformat)

    return parsed_logformats + [default]


def get_logformat(root_config: RootNginxConfig, line: str) -> re.Pattern:
    """
    Find the matching Nginx log_format. If not found, raise an exception
    """
    logformats = get_all_nginx_logformats(root_config)
    for logformat in logformats:
        pattern = logformat_to_regex_pattern(logformat)
        if pattern and pattern.match(line):
            return pattern

    raise RuntimeError("Could not find matching logformat")


def logformat_to_regex_pattern(log_format: str) -> re.Pattern:
    """
    Convert an Nginx log format to a regex pattern.
    Nginx allows for variables like $http_host. This can be filled
    in with any symbol.
    """
    # Escape all regex special characters like [ ] ( ) etc.
    escaped_logformat = re.escape(log_format)

    # Replace $http_host with (?P<http_host>.+)
    # Keep the named variables for later parsing
    regex_line_format = re.sub(r"\\\$([\d\w_]+)", "(?P<\\1>.*)", escaped_logformat)
    return re.compile(regex_line_format)


def parse_logline(root_config: RootNginxConfig, line: str) -> dict:
    """
    Parse a log line using a log format.
    """
    # TODO: cache this format and use it for later lines too
    logformat = get_logformat(root_config=root_config, line=line)
    parsed_line = logformat.match(line)

    if not parsed_line:
        raise RuntimeError("Couldn't parse logline")
    return parsed_line.groupdict()
