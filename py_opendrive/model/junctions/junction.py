from dataclasses import dataclass
from typing import Optional


@dataclass
class Junction:
    id: str
    name: Optional[str] = None
