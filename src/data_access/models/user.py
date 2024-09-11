from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from . import (
    models,
)


class User(models.Model):
    __tablename__ = "users"

    first_name: Mapped[str]
    last_name: Mapped[str] = mapped_column(unique=True, nullable=True)
    email: Mapped[str] = mapped_column(unique=True, nullable=True)
