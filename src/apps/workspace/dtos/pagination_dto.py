from dataclasses import dataclass


@dataclass
class PaginationDTO:
    page: int
    page_size: int
