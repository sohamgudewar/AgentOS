from pathlib import Path

from pypdf import PdfReader


class DocumentExtractor:
    """Extract text from uploaded documents."""

    @staticmethod
    def extract(file_path: str) -> str:
        path = Path(file_path)

        suffix = path.suffix.lower()

        if suffix == ".txt":
            return path.read_text(
                encoding="utf-8",
            )

        if suffix == ".pdf":
            reader = PdfReader(path)

            text = ""

            for page in reader.pages:
                text += page.extract_text() or ""

                return text

        raise ValueError(
            f"Unsupported file type: {suffix}"
        )
