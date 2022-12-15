import re
from pathlib import Path
from typing import Any, Generator, List, Optional, Tuple, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


def compare_objects(this: T, that: T, fields: List[str]) -> bool:
    for field in fields:
        if not getattr(this, field) == getattr(that, field):
            return False
    return True


def filter_unique(line_configs: List["NginxLineConfig"]) -> List["NginxLineConfig"]:
    """
    Filter out lines that are already covered by a parent.
    """
    filtered_lines = []
    for line_config in line_configs:
        if not line_config in filtered_lines:
            filtered_lines.append(line_config)
    return filtered_lines


def get_children_recursive(line_config: "NginxLineConfig") -> List["NginxLineConfig"]:
    """
    Get all children of a line recursively.
    """
    children = []
    for child in line_config.children:
        children.append(child)
        children.extend(get_children_recursive(child))
    return children


def get_parents_recursive(line_config: "NginxLineConfig") -> List["NginxLineConfig"]:
    """
    Get all parents of a line recursively.
    """
    parents = []
    current_line = line_config
    while current_line.parent:
        parents.append(current_line.parent)
        current_line = current_line.parent

    return parents


class DirectiveFilter(BaseModel):
    directive: str
    value: Optional[str] = None

    def match(self, line: "NginxLineConfig") -> bool:
        """
        A block matches if the block itself matches or all filters apply
        to any of the children beneath it matches.
        """
        if line.directive == self.directive:
            if self.value is None or self.value in line.args:
                return True
        return False

    def __hash__(self) -> int:
        return hash(str(self))

    def __str__(self) -> str:
        return f"{self.directive} -> {self.value}"


class NginxLineConfig(BaseModel):
    directive: str
    line: int
    args: List[str]
    file: Optional[Path]  # Only filled in after parsing
    block: Optional[List["NginxLineConfig"]]
    parent: Optional["NginxLineConfig"]
    children: List["NginxLineConfig"] = []
    definitely_no_match = False
    full_match = False

    @property
    def lineage(self) -> List[str]:
        if not self.parent:
            return [self.directive]
        return self.parent.lineage + [self.directive]

    @property
    def neighbours(self) -> List["NginxLineConfig"]:
        parent_children = self.parent.children if self.parent else []
        return [c for c in parent_children if c != self]

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, NginxLineConfig):
            return False

        comparison_fields = ["line", "directive", "file", "args"]
        return compare_objects(self, other, comparison_fields)

    # Used for set() operations
    def __hash__(self) -> int:
        return hash(str(self))

    def __str__(self) -> str:
        return f"{self.file}:{self.line} -> {self.directive}"


class NginxFileConfig(BaseModel):
    file: Path
    status: str
    errors: List[str]
    parsed: List[NginxLineConfig]
    included_in: Optional[Tuple["NginxFileConfig", NginxLineConfig]]

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, NginxFileConfig):
            return False

        comparison_fields = ["file", "status", "errors", "parsed"]
        return compare_objects(self, other, comparison_fields)

    def __str__(self) -> str:
        return f"{self.file}"

    @property
    def lines(self) -> Generator[NginxLineConfig, None, None]:
        for line in self.parsed:
            yield line
            for child in get_children_recursive(line):
                yield child


# Fixes the following error:
# `pydantic.errors.ConfigError: field "block" not yet prepared so type is still a ForwardRef, you might need to call NginxLineConfig.update_forward_refs().`
NginxLineConfig.update_forward_refs()


class NginxErrorConfig(BaseModel):
    file: Path
    error: str
    line: int


class RootNginxConfig(BaseModel):
    status: str
    errors: List[NginxErrorConfig]
    config: List[NginxFileConfig]

    @property
    def lines(self) -> Generator[NginxLineConfig, None, None]:
        # After parsing, the root config contains a list of files
        # with lines that are linked to each other. We loop over
        # the lines in the first file, as this is the main config.
        for line_config in self.config[0].lines:
            yield line_config

    def get_files(self, file_path_regex: str) -> List[NginxFileConfig]:
        matching_file_configs = []
        for file_config in self.config:
            if re.match(file_path_regex, str(file_config.file)):
                matching_file_configs.append(file_config)

        if not matching_file_configs:
            # Wildcards are allowed to have no matches
            if "*" not in file_path_regex:
                raise IndexError(f"{file_path_regex} not found in config")

        return matching_file_configs

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, RootNginxConfig):
            return False

        comparison_fields = ["status", "errors", "config"]
        return compare_objects(self, other, comparison_fields)
