"""Tests for Paragraph class."""

from pathlib import Path

import pytest

from dxpars.document import Document
from dxpars.docx_objects.paragraph import Paragraph


@pytest.fixture
def paragraph() -> Paragraph:
    path = str(Path(__file__).parent / 'fixtures' / 'test.docx')
    document = Document(path)
    return document.paragraphs[0]


class TestParagraph:
    """Test Paragraph class."""

    def test_paragraph_text(self, paragraph):
        """Test paragraph text."""
        assert paragraph.text == 'PARAGRAPH WITH TEXT'

    def test_paragraph_properties(self, paragraph):
        """Test paragraph properties."""
        props = paragraph.properties
        assert isinstance(props, dict)
        for prop in ['bold', 'italic', 'caps', 'underline']:
            assert props[prop]

    def test_paragraph_style(self, paragraph):
        """Test paragraph style."""
        assert paragraph.pstyle == 'Style_1'

    def test_paragraph_alignment(self, paragraph):
        """Test paragraph style."""
        assert paragraph.alignment == 'center'
