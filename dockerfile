FROM python:3.14

WORKDIR /revelacion_de_genero

COPY . .

ENV VIRTUAL_ENV=/revelacion_de_genero/.venv_docker
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
ENV PYTHONUNBUFFERED=1

RUN python -m venv $VIRTUAL_ENV

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

CMD ["sh", "-c", "reflex run --env prod --backend-only --backend-port ${PORT:-8000}"]
