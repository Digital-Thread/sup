# :building_construction: Development Instructions

## :books: Table of Contents

- [Installation](#construction_worker-getting-started)
    - [With docker](#construction-with-docker)
    - [Manually](#wheelchair-manually)
- [Tests](#test_tube-tests)

## :construction_worker: Getting Started

First, rename the file `.env.template` to `.env`\
Afterward, fill it with the required data.

| Variable          | Type | Importance | Description                                                                                  |
|-------------------|------|------------|----------------------------------------------------------------------------------------------|
| POSTGRES_USER     | str  | True       | Username of the database owner                                                               |
| POSTGRES_PASSWORD | str  | True       | Password from the database                                                                   |
| POSTGRES_DB       | str  | True       | Database name                                                                                |
| DB_HOST           | str  | True       | IP address of the database (Name of the service in the docker-compose.yml (Use `postgres`)). |
| DB_PORT           | str  | True       | The database port. Usually the db running on port `5432`                                     |
| REDIS_PASSWORD    | str  | False      | Password for the Redis database                                                              |
| REDIS_PORT        | int  | False      | The port on which the Redis server is running, typically `6379`                              |
| REDIS_HOST        | str  | False      | The IP address or hostname of the Redis server                                               |
| SMTP_HOST         | str  | True       | The hostname or IP address of the SMTP server                                                |
| SMTP_PORT         | str  | True       | The port on which the SMTP server is running                                                 |
| SMTP_PASS         | str  | True       | The password for the SMTP server                                                             |
| SMTP_EMAIL        | str  | True       | The email address used for SMTP authentication                                               |
| SMTP_TLS          | bool | True       | whether to use TLS for SMTP communication (e.g., true or false)                              |
| SECRET_KEY        | str  | True       | 	a secret key used for securely signing tokens and other security-related operations         |
| ALGORITHM         | str  | True       | the algorithm used for encoding and decoding tokens (e.g., HS256 for HMAC SHA256)            |

### :construction: With docker

If the application is running in Docker, `DB_HOST` should be set to `postgres`

If the application is running in Docker, `DB_PORT` should be set to `5432`

---

First clone the repository

```shell
$ git clone https://github.com/DavidRomanovizc/DatingBot.git
```

Once done, run the following command:

```shell
$ docker-compose build
```

### :wheelchair: Manually

If you prefer not to use Docker, you can manually build the app.
Before clone the repository, ensure Python is installed:

```sh
$ python -V
```

If Python is installed, clone the repository:

```sh
$ git clone https://github.com/DavidRomanovizc/DatingBot.git
```

Create a virtual environment:

```sh
$ python -m venv venv
```

Activate the virtual environment:

<u>On Windows:</u>

```sh
$ venv\Scripts\activate
```

<u>On macOS and Linux:</u>

```sh
$ source venv/bin/activate
```

After setting up the virtual environment,
install [Poetry](https://python-poetry.org/docs/#installing-with-the-official-installer)

Then install dependencies:

```shell
$ poetry install
```

Run the following commands to make migrations:

```sh
$ alembic upgrade heads
```

## :test_tube: Tests

Звук сверчков и перекати-поле...