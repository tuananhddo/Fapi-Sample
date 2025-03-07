FROM python:3.12

WORKDIR /workdir
ENV PYTHONPATH "${PYTHONPATH}:/workdir/src"
ENV POETRY_VIRTUALENVS_CREATE=false
ENV POETRY_VIRTUALENVS_IN_PROJECT=true
ENV POETRY_NO_INTERACTION=1

RUN pip install poetry

COPY src ./src
COPY migrations ./migrations
COPY ./alembic.ini .
COPY ./pyproject.toml .
COPY ./poetry.lock .
COPY ./gunicorn.conf.py .

RUN poetry install --only main --no-root --no-interaction --no-ansi \
  && rm -rf "./.cache"

CMD ["gunicorn", "--config", "./gunicorn.conf.py", "src.main:app"]