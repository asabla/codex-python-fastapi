from fastapi.testclient import TestClient
from pypdf import PdfWriter
from app.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}

def test_count_pages(tmp_path):
    pdf_path = tmp_path / "dummy.pdf"
    writer = PdfWriter()
    writer.add_blank_page(width=72, height=72)
    with open(pdf_path, "wb") as f:
        writer.write(f)
    with open(pdf_path, "rb") as f:
        response = client.post("/pdf/pages", files={"file": ("dummy.pdf", f, "application/pdf")})
    assert response.status_code == 200
    assert response.json() == {"pages": 1}


def test_upload_pdf(tmp_path):
    """Uploading a non-empty PDF should succeed."""
    pdf_path = tmp_path / "upload.pdf"
    writer = PdfWriter()
    writer.add_blank_page(width=72, height=72)
    with open(pdf_path, "wb") as f:
        writer.write(f)
    with open(pdf_path, "rb") as f:
        response = client.post(
            "/upload",
            files={"file": ("upload.pdf", f, "application/pdf")},
        )
    assert response.status_code == 200
    json_resp = response.json()
    assert json_resp["filename"] == "upload.pdf"
    assert json_resp["size"] > 0


def test_upload_invalid_type(tmp_path):
    txt_path = tmp_path / "bad.txt"
    txt_path.write_text("hello")
    with open(txt_path, "rb") as f:
        response = client.post(
            "/upload",
            files={"file": ("bad.txt", f, "text/plain")},
        )
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid file type"


def test_upload_empty_file(tmp_path):
    empty_path = tmp_path / "empty.pdf"
    empty_path.write_bytes(b"")
    with open(empty_path, "rb") as f:
        response = client.post(
            "/upload",
            files={"file": ("empty.pdf", f, "application/pdf")},
        )
    assert response.status_code == 400
    assert response.json()["detail"] == "Empty file"
