import fitz  # PyMuPDF

async def extract_text_from_pdf(file) -> str:
    """Extract text from an uploaded PDF file."""
    contents = await file.read()
    file_path = f"temp_{file.filename}"
    with open(file_path, "wb") as f:
        f.write(contents)

    text = ""
    pdf_document = fitz.open(file_path)
    for page in pdf_document:
        text += page.get_text()

    return text
