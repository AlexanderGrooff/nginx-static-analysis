from typing import List

from nginx_analysis.dataclasses import AllFilter, CombinedFilters, DirectiveFilter


def args_to_filter(filter_args: List[str]) -> CombinedFilters:
    directives = [f.split("=")[0] for f in filter_args]
    values = ["".join(f.split("=")[1:]) for f in filter_args]
    return AllFilter(
        filters=[
            DirectiveFilter(directive=d, value=v) for d, v in zip(directives, values)
        ]
    )


def logline_to_filter(logline: dict) -> CombinedFilters:
    filters = AllFilter()
    if "server_name" in logline:
        filters += DirectiveFilter(
            directive="server_name", value=logline["server_name"]
        )
    if "request" in logline:
        try:
            location = logline["request"].split(" ")[1]
        except IndexError:
            pass
        else:
            filters += DirectiveFilter(directive="location", value=location)

    return filters
