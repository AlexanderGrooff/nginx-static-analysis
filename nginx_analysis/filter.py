from typing import List, Optional

from nginx_analysis.dataclasses import (
    AllFilter,
    AnyFilter,
    CombinedFilters,
    DirectiveFilter,
)


def args_to_filter(
    directives: List[str], values: List[Optional[str]]
) -> CombinedFilters:
    if len(values) > len(directives):
        raise RuntimeError(f"Found more values than directives")

    if len(directives) > len(values):
        if len(directives) == len(values) + 1:
            values.append(None)
        else:
            raise RuntimeError(f"Found more than one directive without value")

    return AnyFilter(
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
