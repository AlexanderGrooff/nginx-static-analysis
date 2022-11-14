from typing import List

from loguru import logger
from prettytable import PrettyTable

from nginx_analysis.dataclasses import NginxLineConfig


def render_directive_matches(directive_matches: List[NginxLineConfig]):
    headers = ["File", "Values", "Directives"]
    directives_table = PrettyTable(headers)
    for line_config in directive_matches:
        logger.debug(f"Rendering line config {line_config}")
        file_line = f"{line_config.file}:{line_config.line}"
        values = " ".join(line_config.args)
        parent_blocks = " -> ".join(line_config.lineage)
        directives_table.add_row([file_line, values, parent_blocks])

    logger.info(directives_table)
