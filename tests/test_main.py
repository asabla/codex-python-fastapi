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
