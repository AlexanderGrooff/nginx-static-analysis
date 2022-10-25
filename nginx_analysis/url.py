from typing import List, Optional
from urllib.parse import urlparse

from loguru import logger

from nginx_analysis.analysis import get_directive_matches, get_lines_matching_filter
from nginx_analysis.dataclasses import (
    CombinedFilters,
    DirectiveFilter,
    NginxLineConfig,
    RootNginxConfig,
)


def get_parent_server_block(line_config: NginxLineConfig) -> NginxLineConfig:
    if line_config.directive == "server" or not line_config.parent:
        return line_config
    return get_parent_server_block(line_config.parent)


def get_server_configs(
    config: RootNginxConfig, port: Optional[int]
) -> List[NginxLineConfig]:
    listen_directives = get_directive_matches(
        config, CombinedFilters(filters=[DirectiveFilter(directive="listen")])
    )
    server_configs = []
    for d in listen_directives:
        if (port is None) or (str(port) in d.args):
            # Return server block, not listen block
            server_block = get_parent_server_block(d)
            server_configs.append(server_block)
    return server_configs


def get_default_servers(
    config: RootNginxConfig, port: Optional[int]
) -> List[NginxLineConfig]:
    # Look for default_server in listen directives
    listen_directives = get_directive_matches(
        config, CombinedFilters(filters=[DirectiveFilter(directive="listen")])
    )
    server_configs = []
    for d in listen_directives:
        if ((port is None) or (str(port) in d.args)) and "default_server" in d.args:
            # Return server block, not listen block
            server_block = get_parent_server_block(d)
            server_configs.append(server_block)
    return server_configs


def get_port_for_url(url: str) -> Optional[int]:
    # Port is only parsed with valid scheme
    parsed_url = urlparse(_prefix_url(url))
    if parsed_url.port:
        return parsed_url.port

    parsed_url = urlparse(url)
    if parsed_url.scheme == "http":
        return 80

    if parsed_url.scheme == "https":
        return 443

    logger.debug(f"Couldn't find port on url {url}")
    return None


def _prefix_url(url: str) -> str:
    if not (url.startswith("http://") or url.startswith("https://")):
        # Required for proper parsing with urlparse
        url = f"http://{url}"
    return url


def get_server_configs_for_url(
    url: str, config: RootNginxConfig
) -> List[NginxLineConfig]:
    url_domain = urlparse(_prefix_url(url)).netloc
    url_port = get_port_for_url(url)
    logger.debug(f"Looking for url {url_domain} with port {url_port}")
    server_name_configs = get_server_configs(config, url_port)

    url_server_config = []

    # Override url server config if it's identical to an existing server name
    for server_config in server_name_configs:
        server_name_configs = get_lines_matching_filter(
            CombinedFilters(filters=[DirectiveFilter(directive="server_name")]),
            line_config=server_config,
        )
        for server_name_config in server_name_configs:
            if url_domain in server_name_config.args:
                logger.debug(f"Matched server config in {server_config.file}")
                url_server_config.append(server_config)

    if not url_server_config:
        # Default to the default server config
        url_server_config = get_default_servers(config, url_port)
        if url_server_config:
            logger.debug(f"No specific matches found. Using default server")
    return url_server_config
