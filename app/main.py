from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi_health import health
from pypdf import PdfReader
from pypdf.errors import PdfReadError


ALLOWED_TYPES = {"application/pdf", "image/png", "text/markdown"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

app = FastAPI()


def healthy() -> bool:
    """Simple health check condition."""
    return True


app.add_api_route("/health", health([healthy]))


@app.post("/pdf/pages")
async def count_pages(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Invalid content type")

    # Read file content instead of checking length directly
    contents = await file.read()
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File too large")

    try:
        # Create a PdfReader from the contents
        from io import BytesIO

        reader = PdfReader(BytesIO(contents))
        pages = len(reader.pages)
        return {"pages": pages}
    except PdfReadError:
        raise HTTPException(status_code=400, detail="Invalid PDF file")


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """Upload a file ensuring it's not empty and has an allowed type."""
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=400,
            detail="Invalid file type",
        )

    # Read file content
    contents = await file.read()
    total_size = len(contents)

    if total_size > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File too large")

    if not contents:
        raise HTTPException(status_code=400, detail="Empty file")

    return {"filename": file.filename, "size": total_size}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
