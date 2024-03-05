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
## Run
poetry run uvicorn main:app --reload