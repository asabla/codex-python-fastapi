# codex-python-fastapi

This project demonstrates a basic FastAPI application managed with [uv](https://github.com/astral-sh/uv).

## Development

Install all dependencies and create the virtual environment:

```bash
uv sync
```

Add new dependencies with:

```bash
uv add <package>
```

Run the application locally:

```bash
uvicorn app.main:app --reload
```

Run the tests:

```bash
uv run python -m pytest
```

## API

- `GET /` – returns a simple greeting
- `POST /pdf/pages` – upload a PDF file and get the page count
