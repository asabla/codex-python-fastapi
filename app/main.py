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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
