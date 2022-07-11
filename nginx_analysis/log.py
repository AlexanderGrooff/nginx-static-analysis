import re


def get_nginx_logformat() -> str:
    """
    Parse the logformat from the Nginx config.
    Defaults to the 'combined' logformat if none
    were found.
    """
    # TODO: Find logformat by parsing the 'log_format' directive
    return (
        "$remote_addr - $remote_user [$time_local] "
        '"$request" $status $body_bytes_sent '
        '"$http_referer" "$http_user_agent"'
    )


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
    regex_line_format = re.sub(r"\\\$([\d\w_]+)", "(?P<\\1>.+)", escaped_logformat)
    return re.compile(regex_line_format)


def parse_logline(line: str) -> dict:
    """
    Parse a log line using a log format.
    """
    nginx_logformat = get_nginx_logformat()
    logformat_pattern = logformat_to_regex_pattern(nginx_logformat)
    parsed_line = logformat_pattern.match(line)
    if not parsed_line:
        raise RuntimeError("Could not parse logline")
    return parsed_line.groupdict()
