FROM python:3.12-slim-trixie AS base

ENV PYTHONUNBUFFERED=1 \
    PATH="/service/.venv/bin:$PATH"

WORKDIR /service


FROM base AS builder

COPY --from=ghcr.io/astral-sh/uv:0.11 /uv /bin/uv

ENV UV_LINK_MODE=copy

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project


FROM base AS runtime

COPY --from=builder /service/.venv /service/.venv

COPY app ./app

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
