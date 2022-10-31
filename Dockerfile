FROM python:3.11

WORKDIR /code

RUN pip install poetry

COPY ./pyproject.toml ./poetry.lock /code/

RUN poetry config virtualenvs.create false

RUN poetry install --no-root

COPY . /code

RUN poetry install

#CMD ["uvicorn", "src.streaming.main:app", "--host", "0.0.0.0", "--port", "80"]

# If running behind a proxy like Nginx or Traefik add --proxy-headers
 CMD ["uvicorn", "src.streaming.main:app", "--host", "0.0.0.0", "--port", "80", "--proxy-headers"]