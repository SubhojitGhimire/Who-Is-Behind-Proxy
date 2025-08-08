from enum import Enum
from dataclasses import dataclass

class ProxyStatus(str, Enum):
    FUNCTIONAL = "✅ Functional"
    NOT_FUNCTIONAL = "❌ Not Functional"
    ERROR = "⚠️ Proxy Error"
    INVALID_RESPONSE = "❓ Invalid Response"
    UNTESTED = "⚪ Untested"

@dataclass
class Proxy:
    protocol: str
    host: str
    port: int
    status: ProxyStatus = ProxyStatus.UNTESTED

    @property
    def url(self) -> str:
        return f"{self.protocol}://{self.host}:{self.port}" # Returns the full proxy URL.

    @property
    def address(self) -> str:
        return f"{self.host}:{self.port}" # Returns the host:port combination.