FROM python:3.12-alpine  AS builder

COPY poetry.lock pyproject.toml ./
RUN python -m pip install --no-cache-dir poetry==1.4.2 \
    && poetry export --without-hashes --without dev,test -f requirements.txt -o requirements.txt

FROM python:3.12-alpine

COPY --from=builder requirements.txt ./
RUN python -m pip install --no-cache-dir -r requirements.txt

COPY . ./

ENV PYTHONPATH "${PYTHONPATH}:/Hoz_bot"

#RUN alembic upgrade head
#CMD ["./scripts/makemigrations.sh"]
#CMD ["./scripts/migrate.sh"]
CMD ["python3", "/hozbot/main.py"]