FROM python:3.9.16-slim-bullseye

COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

COPY ./osrs_gept /app/osrs_gept
WORKDIR /app

ENTRYPOINT ["uvicorn", "osrs_gept.main:app"]
