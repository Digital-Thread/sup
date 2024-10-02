import dataclasses

from environs import Env
from sqlalchemy import URL


@dataclasses.dataclass(frozen=True, slots=True)
class RedisConfig:
    """
    Redis configuration class.

    Attributes
    ----------
    password : Optional(str)
        The password used to authenticate with Redis.
    port : Optional(int)
        The port where Redis server is listening.
    host : Optional(str)
        The host where Redis server is located.
    """

    host: str | None
    port: int | None
    password: str | None

    @staticmethod
    def from_env(env: Env) -> 'RedisConfig':
        """
        Creates the RedisConfig object from environment variables.
        """
        password = env.str('REDIS_PASSWORD', None)
        port = env.int('REDIS_PORT', None)
        host = env.str('REDIS_HOST', None)

        return RedisConfig(password=password, port=port, host=host)

    @property
    def construct_redis_dsn(self) -> str:
        """
        Constructs and returns a Redis DSN (Data Source Name) for this database configuration.
        """
        if self.password:
            return f'redis://:{self.password}@{self.host}:{self.port}/0'
        else:
            return f'redis://{self.host}:{self.port}/0'


@dataclasses.dataclass(frozen=True, slots=True)
class DbConfig:
    """
    Database configuration class.
    This class holds the settings for the database, such as host, password, port, etc.

    Attributes
    ----------
    host : str
        The host where the database server is located.
    password : str
        The password used to authenticate with the database.
    user : str
        The username used to authenticate with the database.
    database : str
        The name of the database.
    port : int
        The port where the database server is listening.
    """

    host: str
    password: str
    user: str
    database: str
    port: int
    naming_convention = {
        'ix': 'ix_%(column_0_label)s',
        'uq': 'uq_%(table_name)s_%(column_0_N_name)s',
        'ck': 'ck_%(table_name)s_%(constraint_name)s',
        'fk': 'fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s',
        'pk': 'pk_%(table_name)s',
    }

    @staticmethod
    def from_env(env: Env) -> 'DbConfig':
        """
        Creates the DbConfig object from environment variables.
        """
        host = env.str('DB_HOST')
        password = env.str('POSTGRES_PASSWORD')
        user = env.str('POSTGRES_USER')
        database = env.str('POSTGRES_DB')
        port = env.int('DB_PORT', 5432)

        return DbConfig(
            host=host,
            password=password,
            user=user,
            database=database,
            port=port,
        )

    @property
    def construct_sqlalchemy_url(
        self,
        driver: str = 'asyncpg',
        host: str | None = None,
        port: int | None = None,
    ) -> str:
        """
        Constructs and returns a SQLAlchemy URL for this database configuration.
        """
        if not host:
            host = self.host
        if not port:
            port = self.port
        uri = URL.create(
            drivername=f'postgresql+{driver}',
            username=self.user,
            password=self.password,
            host=host,
            port=port,
            database=self.database,
        )
        return uri.render_as_string(hide_password=False)

    @property
    def construct_psql_dns(self) -> str:
        uri = URL.create(
            drivername='postgresql',
            username=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
            database=self.database,
        )
        return uri.render_as_string(hide_password=False)


@dataclasses.dataclass(frozen=True, slots=True)
class SMTPConfig:
    host: str
    port: int
    password: str
    email: str
    TLS: bool = True

    @staticmethod
    def from_env(env: Env) -> 'SMTPConfig':
        host = env.str('SMTP_HOST')
        port = env.int('SMTP_PORT')
        password = env.str('SMTP_PASS')
        email = env.str('SMTP_EMAIL')
        return SMTPConfig(
            host=host,
            port=port,
            password=password,
            email=email,
        )


@dataclasses.dataclass(frozen=True, slots=True)
class Miscellaneous:
    """
    Miscellaneous settings class.

    This class holds settings that don't fit into other categories.
    """

    pass

    @staticmethod
    def from_env(env: Env) -> 'Miscellaneous':
        return Miscellaneous()


@dataclasses.dataclass(frozen=True, slots=True)
class Config:
    """
    The main configuration class that integrates all the other configuration classes.

    This class holds the other configuration classes,
    providing a centralized point of access for all settings.

    Attributes
    ----------
    db: Optional[DbConfig]
        Holds the settings specific to the database (default is None).
    """

    db: DbConfig
