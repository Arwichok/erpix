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
    DEBUG=True uv run litestar run -r

serve:
    uv run litestar run

build:
    npx vite build
    npx @tailwindcss/cli -i {{TAILWIND_INPUT}} -o {{TAILWIND_OUTPUT}} --minify

dev-all:
    npx concurrently "just css" "just dev"
