from typing import List

from nginx_analysis.dataclasses import DirectiveFilter


def args_to_filter(filter_args: List[str]) -> List[DirectiveFilter]:
    directives = [f.split("=")[0] for f in filter_args]
    values = ["".join(f.split("=")[1:]) for f in filter_args]
    return [DirectiveFilter(directive=d, value=v) for d, v in zip(directives, values)]


def logline_to_filter(logline: dict) -> List[DirectiveFilter]:
    filters: List[DirectiveFilter] = []
    if "server_name" in logline:
        filters.append(
            DirectiveFilter(directive="server_name", value=logline["server_name"])
        )
    if "request" in logline:
        try:
            location = logline["request"].split(" ")[1]
        except IndexError:
            pass
        else:
            filters.append(DirectiveFilter(directive="location", value=location))

    return filters
