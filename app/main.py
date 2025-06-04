from fastapi import FastAPI, UploadFile, File
from pypdf import PdfReader

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Hello World"}

@app.post("/pdf/pages")
async def count_pages(file: UploadFile = File(...)):
    reader = PdfReader(file.file)
    pages = len(reader.pages)
    return {"pages": pages}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
