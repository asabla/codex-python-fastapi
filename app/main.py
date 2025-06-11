from fastapi import FastAPI, UploadFile, File, HTTPException
from pypdf import PdfReader
from pypdf.errors import PdfReadError

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Hello World"}

@app.post("/pdf/pages")
async def count_pages(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Invalid content type")
    try:
        reader = PdfReader(file.file)
        pages = len(reader.pages)
        return {"pages": pages}
    except PdfReadError:
        raise HTTPException(status_code=400, detail="Invalid PDF file")


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """Upload a file ensuring it's not empty and has an allowed type."""
    allowed_types = {"application/pdf", "image/png", "text/markdown"}
    if file.content_type not in allowed_types:
        raise HTTPException(status_code=400, detail="Invalid file type")

    contents = await file.read()
    if not contents:
        raise HTTPException(status_code=400, detail="Empty file")

    return {"filename": file.filename, "size": len(contents)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
