FROM python:3.11

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /projectx


COPY poetry.lock pyproject.toml /projectx/
RUN pip install poetry
RUN poetry install --no-root

COPY src/ /projectx/src/

EXPOSE 8000

CMD ["poetry", "run", "python", "-m", "uvicorn", "src.app.app:app", "--host", "0.0.0.0"]
