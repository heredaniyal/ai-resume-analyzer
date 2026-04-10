"""
File Parser Service - Extracts text from uploaded resume files

This service handles PDF and Word (.docx) files.
When a user uploads a resume, this code extracts the text content
so it can be sent to the AI for analysis.

Supported formats:
- PDF files (.pdf)
- Word documents (.docx)
"""

import io
from fastapi import UploadFile, HTTPException
from PyPDF2 import PdfReader
from docx import Document


class FileParser:
    """
    Extracts text from various file formats.

    Usage example:
        parser = FileParser()
        text = await parser.extract_text(uploaded_file)
    """

    # Supported file extensions and their MIME types
    SUPPORTED_FILES = {
        "application/pdf": [".pdf"],
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document": [".docx"],
    }

    def __init__(self):
        pass

    async def extract_text(self, file: UploadFile) -> str:
        """
        Main method to extract text from an uploaded file.

        Args:
            file: The uploaded file (from FastAPI's UploadFile)

        Returns:
            str: The extracted text content

        Raises:
            HTTPException: If file type is not supported or file is empty
        """

        # Step 1: Check if file type is supported
        if file.content_type not in self.SUPPORTED_FILES:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file type: {file.content_type}. "
                       f"Supported types: PDF, DOCX"
            )

        # Step 2: Read the file content
        file_content = await file.read()

        if not file_content:
            raise HTTPException(
                status_code=400,
                detail="Uploaded file is empty"
            )

        # Step 3: Extract text based on file type
        try:
            if file.content_type == "application/pdf":
                return self._extract_from_pdf(file_content)
            elif file.content_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                return self._extract_from_docx(file_content)
            else:
                # This shouldn't happen due to earlier check, but included for safety
                raise HTTPException(
                    status_code=400,
                    detail=f"Cannot extract text from {file.content_type}"
                )
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to parse file: {str(e)}"
            )

    def _extract_from_pdf(self, file_content: bytes) -> str:
        """
        Extract text from a PDF file.

        How it works:
        1. Create a file-like object from the bytes
        2. Use PyPDF2 to read the PDF
        3. Extract text from each page
        4. Combine all pages into one text
        """
        try:
            # Create a file-like object from bytes
            pdf_file = io.BytesIO(file_content)

            # Read the PDF
            reader = PdfReader(pdf_file)

            # Extract text from each page
            text_parts = []
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    text_parts.append(text)

            # Combine all pages
            return "\n\n".join(text_parts)

        except Exception as e:
            raise Exception(f"PDF extraction failed: {str(e)}")

    def _extract_from_docx(self, file_content: bytes) -> str:
        """
        Extract text from a Word (.docx) file.

        How it works:
        1. Create a file-like object from the bytes
        2. Use python-docx to read the document
        3. Extract text from each paragraph
        4. Combine all paragraphs
        """
        try:
            # Create a file-like object from bytes
            docx_file = io.BytesIO(file_content)

            # Read the Word document
            doc = Document(docx_file)

            # Extract text from paragraphs
            text_parts = []
            for paragraph in doc.paragraphs:
                if paragraph.text.strip():
                    text_parts.append(paragraph.text)

            # Combine all paragraphs
            return "\n\n".join(text_parts)

        except Exception as e:
            raise Exception(f"DOCX extraction failed: {str(e)}")
