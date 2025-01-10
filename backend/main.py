from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
# List of allowed origins (add your frontend URL here)
import os

UPLOAD_DIR = "uploaded_files"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

app = FastAPI()
origins = [
    "http://localhost:3000",  # Allow requests from Next.js dev server
]

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # List of allowed origins
    allow_credentials=True,  # Allow cookies to be included
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)
@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI"}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        # Read file content (optional)
        content = await file.read()
        # Save file or process it
        with open(f"uploaded_files/{file.filename}", "wb") as f:
            f.write(content)

        return JSONResponse(content={"filename": file.filename, "message": "File uploaded successfully"})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)