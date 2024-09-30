# from dataclasses import dataclass


# @dataclass(eq=False)
# class ApplicationError(Exception):
#     """Base error"""

#     status_code: int = 500
#     message: str = 'Internal Server Error'

#     def __post_init__(self):
#         super().__init__(self.message)


class ApplicationError(Exception):
    """Base error"""

    def __init__(
        self,
        status_code: int = 500,
        message: str = 'Internal Server Error',
    ):
        self.status_code = status_code
        self.message = message
        super().__init__(self.message)
