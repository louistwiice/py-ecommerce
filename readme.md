# Project Name: GraphQL Backend API

## Description
The goal is to have a base project backend In GraphQL. The project run on docker

## Settings
* Postgresql
* Redis

## Run projects

Please follow this part to start the project

### .env file for postgresql in .envs/.env.postgres
| Variable          | Description            | Default    |
|-------------------|------------------------|------------|
| POSTGRES_USER     | Postgres USERNAME      | test       |
| POSTGRES_PASSWORD | Postgres password      | passer1234 |
| POSTGRES_DB       | Postgres Database name | graphql    |
| POSTGRES_HOST     | Postgres host          | potsgres   |
| POSTGRES_PORT     | Postgres port          | 5432       |

### .env file for the app in .envs/.env.app
| Variable               | Description                                                                    | Default                                        | Example             |
|------------------------|--------------------------------------------------------------------------------|------------------------------------------------|---------------------|
| DEBUG                  | To activate Debug                                                              | True                                           |                     |
| SECRET_KEY             | Django secret key                                                              |                                                | my-secret-key-value |
| EMAIL_BACKEND          | Email Backend                                                                  | django.core.mail.backends.console.EmailBackend | 584                 |
| EMAIL_PORT             | Email Port                                                                     | 1025                                           | 584                 |
| EMAIL_HOST             | Email host                                                                     | mailhog                                        | smtp.gmail.com      |
| EMAIL_USE_TLS          | Use TLS when sending email                                                     | False                                          |                     |
| EMAIL_HOST_USER        | Email user                                                                     | example@example.com                            |                     |
| EMAIL_HOST_PASSWORD    | Email password                                                                 | None                                           |                     |
| LOG_FORMATTER          | Way to print your log. Colored (colored_formatter) or in JSON (json_formatter) | colored_formatter                              |                     |
| REDIS_DEFAULT_CACHE_DB | Default Database for Django cache                                              | 5                                              | 0                   |

