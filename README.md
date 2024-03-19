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

#Document
https://fastapi.tiangolo.com/learn/
https://github.com/zhanymkanov/fastapi-best-practices?tab=readme-ov-file#17-save-files-in-chunks