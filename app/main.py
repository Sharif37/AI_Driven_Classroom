from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from app.routes import upload
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for security as needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the router for your upload route
app.include_router(upload.router)

# Serve static files (HTML, CSS, JavaScript) from the "static" directory
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Route to serve the HTML form
@app.get("/upload-form/", response_class=HTMLResponse)
async def serve_html_form():
    with open("app/static/upload_form.html", "r") as f:
        content = f.read()
    return HTMLResponse(content=content)
