FROM ghcr.io/astral-sh/uv:alpine

ENV BOT_TOKEN=

COPY . .

RUN uv sync

ENTRYPOINT [ "uv", "run", "main.py" ]
