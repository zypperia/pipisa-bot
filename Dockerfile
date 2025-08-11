FROM ghcr.io/astral-sh/uv:alpine

ENV BOT_TOKEN=
ENV REDIS_HOST=

COPY . .

RUN uv sync

ENTRYPOINT [ "uv", "run", "main.py" ]
