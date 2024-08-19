# Se crea una imagen de Docker con la versión de Python 3.12-slim, se instala poetry y se copian los archivos pyproject.toml y poetry.lock para instalar las dependencias del proyecto. Finalmente se copian los archivos del proyecto y se expone el puerto 8000 para que se pueda acceder a la aplicación.

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
