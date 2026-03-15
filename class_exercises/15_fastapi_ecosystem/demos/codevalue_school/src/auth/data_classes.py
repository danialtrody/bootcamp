from dataclasses import dataclass
from typing import Optional


@dataclass(slots=True)
class UserTokenData:
    session_id: str
    exp: int


@dataclass(slots=True)
class SessionFingerprint:
    user_agent: Optional[str]
    ip_address: Optional[str]
