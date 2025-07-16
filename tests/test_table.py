"""Tests for Table class."""

from pathlib import Path

import pytest

from dxpars.document import Document
from dxpars.docx_objects.table import Table


@pytest.fixture
def table() -> Table:
    path = str(Path(__file__).parent / 'fixtures' / 'test.docx')
    document = Document(path)
    return document.tables[0]


class TestTable:
    """Test Table class."""

    def test_table_shape(self, table):
        """Test table shape."""

        shape = table.properties['shape']
        assert shape == (2,2)

    def test_table_show(self, table):
        show = table.show
        assert len(show[0]) == 1
        assert len(show[1]) == 2

    def test_table_expand(self, table):
        expand = table.expand
        assert len(expand[0]) == 2
        assert len(expand[1]) == 2
        assert expand[0][0] is expand[0][1]

    def test_row_text(self, table):
        text = table.parts[0].text
        assert len(text.split('\t')) == 2


class TestCell:
    """Test Cell class."""

    def test_cell_text(self, table):
        """Test cell text."""
        cell_text = table.parts[0].parts[0].text
        assert cell_text == 'Cell 0\nCell 1'

    def test_cell_merge(self, table):
        """Test cell properties."""
        cell_properties = table.parts[0].parts[0].properties
        assert cell_properties['h_merge'] == 2

    def test_cell_with_table(self, table):
        """Test cell merge information."""
        cell_table = table.parts[1].parts[1].parts[1]
        assert isinstance(cell_table, Table)
        assert len(cell_table.text) > 0
        assert len(cell_table.parts) == 2
