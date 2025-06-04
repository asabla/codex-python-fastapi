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

## Continuous Integration

The project includes a GitHub Actions workflow that automatically runs the
tests for every push and pull request. The workflow definition lives in
`.github/workflows/ci.yml`.

## API

- `GET /` – returns a simple greeting
- `POST /pdf/pages` – upload a PDF file and get the page count
