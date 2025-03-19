FROM python:3.10-slim-bookworm
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /workspace/backend

COPY .python-version pyproject.toml uv.lock ./

RUN uv sync --frozen

EXPOSE 8000

CMD [ "uv", "run", "uvicorn", "--app-dir", "app", "main:app","--host", "0.0.0.0", "--port", "8000", "--reload" ]