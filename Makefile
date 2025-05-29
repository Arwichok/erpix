

export LITESTAR_HOST=0.0.0.0
export LITESTAR_APP=app.asgi:create_app


vite:
	npx vite

css:
	npx @tailwindcss/cli -i ./src/styles.css -o ./public/bundle.css --watch

dev:
	cd src && uv run litestar run

serve:
	uv run litestar run --host 0.0.0.0


build:
	npx vite build
	npx @tailwindcss/cli -i ./src/styles.css -o ./public/bundle.css --minify
