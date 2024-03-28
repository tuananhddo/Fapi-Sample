# Local Run Guide
## Create Virtual Env (Venv / Conda)
## Install dependencies
## Run Command

# Option 1: Poetry
## Install Poetry
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
Invoke-RestMethod -Uri https://get.scoop.sh | Invoke-Expression
scoop install pipx
pipx ensurepath
pipx install poetry

## Init project
poetry init

## Add Lib / Install
poetry add gino[starlette]
poetry add fastapi uvicorn gunicorn
poetry add -D pytest requests

## DB Migrate
### Go to latest migrations
alembic upgrade head
### Upgrade / Downgrade to specific version
alembic upgrade my-desired-version
alembic downgrade my-desired-version
### Automatic create revision from change of sqlalchemy models
alembic revision --autogenerate -m "Description of changes"

## Run
poetry run uvicorn src.main:app --reload
## Testing
pytest ./src/tests 
# Document
https://fastapi.tiangolo.com/learn/
https://github.com/zhanymkanov/fastapi-best-practices?tab=readme-ov-file#17-save-files-in-chunks


# What project has implemented ?
- Manage package by poetry ( Similar to Nodejs Npm)
- Database interacting by SqlAlchemy
- Database migration with Alembic
- Setup env by dotenv and pydantic
- Example APIs with request/response schema and validation
- Custom OpenAPI
- Authentication
- Add Logger
- Handle Exception

# What will be implement ?
- Paging ( limit /offset or st) <+ Test Autocommit>
- Add Tracer (Jaeger)
- Docker / Production
- Socket
- Testing
- Timezone setup
- Streaming Response
- Lifespan event
- With third-library ( Kafka / S3 / Redis-Logout ...)
- Update DB to SQlAlchemy 2.0 and async / connection pool and SQLModel
    + https://chaoticengineer.hashnode.dev/fastapi-sqlalchemy
    + https://dev.to/akarshan/asynchronous-database-sessions-in-fastapi-with-sqlalchemy-1o7e
    + https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html
# Tips:
- Switch case with additional data
- from array import array
- kwargs /args
- z = [(x, y) for x in xs for y in ys]
