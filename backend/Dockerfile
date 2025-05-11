FROM --platform=linux/amd64 python:3.10-slim-bookworm AS build_amd64
FROM --platform=linux/arm64 python:3.10-slim-bookworm AS build_arm64

FROM build_${TARGETARCH} AS build
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /workspace/backend

COPY . .

RUN rm -rf .venv
RUN uv sync --frozen

EXPOSE 8000

CMD [ "uv", "run", "uvicorn", "--app-dir", "app", "main:app","--host", "0.0.0.0", "--port", "8000", "--reload" ]