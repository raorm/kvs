FROM python:3.8-buster

#System dependencies
RUN pip install "poetry"

WORKDIR /app/

COPY pyproject.toml /app/
COPY poetry.lock /app/

RUN poetry install --no-dev

COPY main.py /app/

EXPOSE 8001 8002 8003

CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0"]
