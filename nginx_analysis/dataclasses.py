import re
from pathlib import Path
from typing import List, Optional, Tuple

from pydantic import BaseModel


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


class NginxFileConfig(BaseModel):
    file: Path
    status: str
    errors: List[str]
    parsed: List[NginxLineConfig]
    included_in: Optional[Tuple["NginxFileConfig", NginxLineConfig]]


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

    def get_file(self, file_path_regex: str) -> NginxFileConfig:
        for file_config in self.config:
            if re.match(file_path_regex, str(file_config.file)):
                return file_config
        raise IndexError(f"{file_path_regex} not found in config")
