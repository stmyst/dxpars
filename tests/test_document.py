"""Tests for Document class."""

from pathlib import Path
from io import BytesIO

import pytest

from dxpars.document import Document
from dxpars.docx_objects.paragraph import Paragraph
from dxpars.docx_objects.table import Table


@pytest.fixture
def test_doc_path():
    """Path to test document."""

    return str(Path(__file__).parent / 'fixtures' / 'test.docx')


@pytest.fixture
def document(test_doc_path):
    """Path to test document."""

    return Document(test_doc_path)


class TestDocument:
    """Test Document class."""

    def test_create_from_path(self, test_doc_path):
        """Test creating Document from file path."""
        doc = Document(test_doc_path)
        assert doc.filename == str(test_doc_path)

    def test_create_from_bytes(self, test_doc_path):
        """Test creating Document from bytes."""
        with open(test_doc_path, 'rb') as f:
            content = f.read()
        
        doc = Document(BytesIO(content), filename='test.docx')
        assert doc.filename == 'test.docx'

    def test_document_parts(self, document):
        """Test document parts."""
        parts = document.parts
        assert isinstance(parts, list)
        assert len(parts) >= 3

        assert isinstance(parts[0], Paragraph)
        assert isinstance(parts[1], Table)
        assert isinstance(parts[2], Paragraph)
        assert isinstance(document.paragraphs, list)
        assert isinstance(document.tables, list)

    def test_document_text(self, document):
        """Test document text."""
        text = document.text
        assert isinstance(text, str)
        assert len(text) > 0

    def test_to_txt(self, test_doc_path):
        document = Document(test_doc_path)
        path = Path(test_doc_path).parent
        doc_names = ['test.txt', 'test1.txt']
        for doc in doc_names:
            if (Path(path) / doc).exists():
                (Path(path) / doc).unlink()

        document.to_txt(folder=str(path))
        document.to_txt(folder=str(path), filename='test1.txt')
        for doc in doc_names:
            assert (Path(path) / doc).exists()
