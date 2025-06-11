set windows-shell := ["C:\\Program Files\\Git\\bin\\sh.exe","-c"]
set dotenv-load


TAILWIND_INPUT := "./src/styles.css"
TAILWIND_OUTPUT := "./public/bundle.css"

export PYTHONPATH := "src"
export LITESTAR_HOST := "0.0.0.0"
export LITESTAR_APP := "app.asgi:create_app"

help:
    just --summary

vite:
    npx vite

css:
    npx @tailwindcss/cli -i {{TAILWIND_INPUT}} -o {{TAILWIND_OUTPUT}} --watch

dev:
    uv run litestar run -r -R src

run:
    uv run litestar run

build:
    npx vite build
    npx @tailwindcss/cli -i {{TAILWIND_INPUT}} -o {{TAILWIND_OUTPUT}} --minify

dev-all:
    npx concurrently "just css" "just dev"


db:
    uv run litestar database

db-up:
    uv run litestar database upgrade

db-down:
    uv run litestar database downgrade

db-drop:
    uv run litestar database drop-all

db-new:
    uv run litestar database make-migrations
