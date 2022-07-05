import re
from pathlib import Path
from typing import Any, List, Optional, Tuple, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


def compare_objects(this: T, that: T, fields: List[str]) -> bool:
    for field in fields:
        if not getattr(this, field) == getattr(that, field):
            return False
    return True


class NginxLineConfig(BaseModel):
    directive: str
    line: int
    args: List[str]
    file: Optional[Path]  # Only filled in after parsing
    block: Optional[List["NginxLineConfig"]]
    parent: Optional["NginxLineConfig"]

    @property
    def parent_blocks(self) -> List[str]:
        if not self.parent:
            return [self.directive]
        return self.parent.parent_blocks + [self.directive]

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, NginxLineConfig):
            return False

        comparison_fields = ["line", "directive", "file", "args"]
        return compare_objects(self, other, comparison_fields)

    def __str__(self) -> str:
        return f"{self.file}:{self.line}"


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

    def get_files(self, file_path_regex: str) -> List[NginxFileConfig]:
        matching_file_configs = []
        for file_config in self.config:
            if re.match(file_path_regex, str(file_config.file)):
                matching_file_configs.append(file_config)

        if not matching_file_configs:
            raise IndexError(f"{file_path_regex} not found in config")

        return matching_file_configs

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, RootNginxConfig):
            return False

        comparison_fields = ["status", "errors", "config"]
        return compare_objects(self, other, comparison_fields)
