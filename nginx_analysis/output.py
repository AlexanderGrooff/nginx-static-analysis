from typing import List, Tuple

from loguru import logger
from prettytable import PrettyTable

from nginx_analysis.dataclasses import NginxFileConfig, NginxLineConfig


def render_directive_matches(
    directive_matches: List[Tuple[NginxFileConfig, NginxLineConfig]]
):
    headers = ["File", "values"]
    directives_table = PrettyTable(headers)
    for file_config, line_config in directive_matches:
        file_line = f"{file_config.file}:{line_config.line}"
        values = " ".join(line_config.args)
        directives_table.add_row([file_line, values])

    logger.info(directives_table)
