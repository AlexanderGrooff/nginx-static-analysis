from typing import List, Optional

from pydantic import BaseModel


class NginxLineConfig(BaseModel):
    directive: str
    line: int
    args: List[str]
    block: Optional[List["NginxLineConfig"]]
    parent: Optional["NginxLineConfig"]
    file_config: Optional["NginxFileConfig"]


class NginxFileConfig(BaseModel):
    file: str
    status: str
    errors: List[str]
    parsed: List[NginxLineConfig]


# Fixes the following error:
# `pydantic.errors.ConfigError: field "block" not yet prepared so type is still a ForwardRef, you might need to call NginxLineConfig.update_forward_refs().`
NginxLineConfig.update_forward_refs()


class RootNginxConfig(BaseModel):
    status: str
    errors: List[str]
    config: List[NginxFileConfig]
