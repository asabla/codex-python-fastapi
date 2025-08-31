import base64
from fastapi.testclient import TestClient
from app.main import app, MAX_FILE_SIZE

client = TestClient(app)


def _write_png(path):
    data = base64.b64decode(
        "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAAAAAA6fptVAAAACklEQVR4nGNgYAAAAAMAASsJTYQAAAAASUVORK5CYII="
    )
    path.write_bytes(data)


def test_upload_png_file(tmp_path):
    png_path = tmp_path / "image.png"
    _write_png(png_path)
    with open(png_path, "rb") as f:
        response = client.post("/upload", files={"file": ("image.png", f, "image/png")})
    assert response.status_code == 200
    assert response.json()["filename"] == "image.png"


def test_upload_markdown_file(tmp_path):
    md_path = tmp_path / "file.md"
    md_path.write_text("# title\n")
    with open(md_path, "rb") as f:
        response = client.post(
            "/upload", files={"file": ("file.md", f, "text/markdown")}
        )
    assert response.status_code == 200
    assert response.json()["filename"] == "file.md"


def test_upload_large_file(tmp_path):
    big_path = tmp_path / "big.pdf"
    big_path.write_bytes(b"x" * (MAX_FILE_SIZE + 1))
    with open(big_path, "rb") as f:
        response = client.post(
            "/upload", files={"file": ("big.pdf", f, "application/pdf")}
        )
    assert response.status_code == 400
    assert response.json()["detail"] == "File too large"


def test_pdf_pages_invalid_content_type(tmp_path):
    png_path = tmp_path / "image.png"
    _write_png(png_path)
    with open(png_path, "rb") as f:
        response = client.post(
            "/pdf/pages", files={"file": ("image.png", f, "image/png")}
        )
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid content type"


def test_pdf_pages_large_file(tmp_path):
    big_path = tmp_path / "big.pdf"
    big_path.write_bytes(b"x" * (MAX_FILE_SIZE + 1))
    with open(big_path, "rb") as f:
        response = client.post(
            "/pdf/pages", files={"file": ("big.pdf", f, "application/pdf")}
        )
    assert response.status_code == 400
    assert response.json()["detail"] == "File too large"
