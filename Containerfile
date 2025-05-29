FROM node:alpine as node


WORKDIR /app

COPY package*.json vite.config.js tailwind.config.js /app/

COPY static/ /app/static
COPY app/templates/ /app/app/templates

RUN --mount=type=bind,source=static/styles.css,target=static/styles.css \
    --mount=type=bind,source=static/main.js,target=static/main.js \
    --mount=type=bind,source=app/templates/,target=app/templates/ \
    npm install && \
    npm run build && \
    npx tailwindcss -i ./static/styles.css -o ./static/dist/output.css --minify


FROM python:alpine as python
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

COPY --from=node /app/static /app/static

COPY app/ /app/app
COPY Makefile /app/

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project

EXPOSE 8000
    
CMD ["uv", "run", "litestar", "run", "--host", "0.0.0.0"]
