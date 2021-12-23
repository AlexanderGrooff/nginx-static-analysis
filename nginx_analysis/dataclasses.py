from typing import List, Optional

from pydantic import BaseModel


class NginxLineConfig(BaseModel):
    directive: str
    line: int
    args: List[str]
    block: Optional[List["NginxLineConfig"]]
    parent: Optional["NginxLineConfig"]
    file_config: Optional["NginxFileConfig"]

    @property
    def parent_blocks(self) -> List[str]:
        if not self.parent:
            return [self.directive]
        return self.parent.parent_blocks + [self.directive]


class NginxFileConfig(BaseModel):
    file: str
    status: str
    errors: List[str]
    parsed: List[NginxLineConfig]
    parent: Optional["NginxFileConfig"]


# Fixes the following error:
# `pydantic.errors.ConfigError: field "block" not yet prepared so type is still a ForwardRef, you might need to call NginxLineConfig.update_forward_refs().`
NginxLineConfig.update_forward_refs()


class NginxErrorConfig(BaseModel):
    file: str
    error: str
    line: int


class RootNginxConfig(BaseModel):
    status: str
    errors: List[NginxErrorConfig]
    config: List[NginxFileConfig]

    def get_file(self, file_path: str) -> NginxFileConfig:
        for file_config in self.config:
            if file_config.file == file_path:
                return file_config
        raise IndexError(f"{file_path} not found in config")
