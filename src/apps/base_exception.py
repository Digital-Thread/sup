import dataclasses
from typing import ClassVar


@dataclasses.dataclass(eq=False)
class ApplicationError(Exception):
    """Base Error"""

    status_code: ClassVar[int] = 500

    @property
    def message(self) -> str:
        return 'An app error occurred'
