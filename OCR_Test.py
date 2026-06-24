
from mistralai.client import Mistral
from pathlib import Path
import os

MISTRAL_API_KEY = os.getenv("")

from mistralai.client import Mistral
from pathlib import Path
import os
import traceback

# ==========================
# CONFIG
# ==========================

# Option 1 (recommended)
MISTRAL_API_KEY = ""
# Option 2 (temporary testing)
# MISTRAL_API_KEY = "PASTE_YOUR_API_KEY_HERE"

if not MISTRAL_API_KEY:
    raise ValueError(
        "MISTRAL_API_KEY environment variable not found"
    )

OCR_MODEL = "mistral-ocr-latest"

client = Mistral(
    api_key=MISTRAL_API_KEY
)


# ==========================
# OCR FUNCTION
# ==========================

def ocr_pdf(pdf_path: str) -> str:

    pdf_path = Path(pdf_path)

    if not pdf_path.exists():
        raise FileNotFoundError(
            f"PDF not found: {pdf_path}"
        )

    print(f"PDF Found: {pdf_path}")
    print(
        f"Size: "
        f"{pdf_path.stat().st_size / 1024 / 1024:.2f} MB"
    )

    try:

        print("Uploading PDF...")

        uploaded_file = client.files.upload(
            file={
                "file_name": pdf_path.name,
                "content": pdf_path.read_bytes(),
            },
            purpose="ocr"
        )

        print("Upload Success")
        print(f"File ID: {uploaded_file.id}")

        print("Generating signed URL...")

        signed_url = client.files.get_signed_url(
            file_id=uploaded_file.id
        )

        print("Running OCR...")

        response = client.ocr.process(
            model=OCR_MODEL,
            document={
                "type": "document_url",
                "document_url": signed_url.url
            }
        )

        markdown_parts = []

        for page in response.pages:

            markdown_parts.append(
                page.markdown or ""
            )

            markdown_parts.append("\n\n")

        return "".join(markdown_parts)

    except Exception:

        print("\nOCR FAILED\n")

        traceback.print_exc()

        raise


# ==========================
# SAVE MARKDOWN
# ==========================

def save_markdown(pdf_path: str):

    markdown_text = ocr_pdf(pdf_path)

    output_path = Path(pdf_path).with_suffix(".md")

    output_path.write_text(
        markdown_text,
        encoding="utf-8"
    )

    print(
        f"\nMarkdown saved:\n{output_path}"
    )


# ==========================
# MAIN
# ==========================

if __name__ == "__main__":

    save_markdown(
        "9780357436479_2.pdf"
    )

