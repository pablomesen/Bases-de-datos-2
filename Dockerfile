# Define la imagen base, workdir, dependencias y comandos para crear y ejecutar la imagen de la aplicación
FROM python:3.12-slim

WORKDIR /app

RUN pip install --no-cache-dir poetry \
  && poetry config virtualenvs.create true \
  && poetry config virtualenvs.in-project true

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-interaction --no-ansi

COPY . .

EXPOSE 8000

CMD ["poetry", "run", "uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8000"]
