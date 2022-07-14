from typing import List, Optional

from nginx_analysis.dataclasses import DirectiveFilter


def args_to_filter(
    directives: List[str], values: List[Optional[str]]
) -> List[DirectiveFilter]:
    if len(values) > len(directives):
        raise RuntimeError(f"Found more values than directives")

    if len(directives) > len(values):
        if len(directives) == len(values) + 1:
            values.append(None)
        else:
            raise RuntimeError(f"Found more than one directive without value")

    return [DirectiveFilter(directive=d, value=v) for d, v in zip(directives, values)]


def logline_to_filters(logline: dict) -> List[DirectiveFilter]:
    filters = []
    if "server_name" in logline:
        filters.append(
            DirectiveFilter(directive="server_name", value=logline["server_name"])
        )
    if "request" in logline:
        location = logline["request"].split(" ")[1]
        filters.append(DirectiveFilter(directive="location", value=location))

    return filters
