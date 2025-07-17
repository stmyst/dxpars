"""docx Table docx_objects."""

from xml.etree import ElementTree

from dxpars.base.base_objects import DocxPart
from dxpars.docx_objects.paragraph import Paragraph
from dxpars.format.table import TableFormat, RowFormat, CellFormat


class Table(DocxPart):
    """Table object."""

    tag = 'tbl'

    def __init__(self, xml_element: ElementTree):
        """
        Create a table  instance.

        Args:
            xml_element: table xml
        """
        super().__init__(
            xml_element=xml_element, formatting=TableFormat, nodes=(Row,),
        )

    @property
    def shape(self) -> tuple[int, int]:
        """Get table shape."""

        return len(self._nodes), self._nodes[0].length

    @property
    def text(self) -> str:
        """Get Table text."""

        return '\n'.join(node.text for node in self._nodes)

    @property
    def show(self) -> dict:
        """Get Table representation as a dict."""

        return {row_idx: row.show for row_idx, row in enumerate(self._nodes)}

    @property
    def properties(self) -> dict:
        """Get Table properties."""

        return {'shape': self.shape}

    @property
    def expand(self) -> dict:
        """Expand horizontally merged cells."""

        return {
            idx: row.expand
            for idx, row in enumerate(self._nodes)
        }


class Row(DocxPart):
    """Row object."""

    tag = 'tr'

    def __init__(self, xml_element: ElementTree):
        """
        Create a table row instance.

        Args:
            xml_element: row xml
        """
        super().__init__(xml_element=xml_element, formatting=RowFormat, nodes=(Cell,))

    @property
    def text(self) -> str:
        """Get Table Row text. Unmerges horizontally merged cells"""

        fixed_width = 10
        return '\t'.join(cell.text.ljust(fixed_width) for cell in self.expand.values())

    @property
    def show(self) -> dict:
        """Return row cells in table structure form."""

        row_cells = {}
        cell_idx = 0
        for cell in self._nodes:
            merged, first = cell.formatting.v_merge
            if merged and not first:
                cell_idx += cell.formatting.h_merge
                continue
            row_cells[cell_idx] = cell.show
            cell_idx += cell.formatting.h_merge
        return row_cells

    @property
    def length(self) -> int:
        """Get Row length."""

        return len(self.expand)

    @property
    def expand(self) -> dict:
        """Expand horizontally merged cells."""

        row_data = {}
        shift = 0
        for cell in self._nodes:
            for _ in range(cell.formatting.h_merge):
                row_data[shift] = cell
                shift += 1
        return row_data

    @property
    def properties(self) -> dict:
        """Get Row properties."""

        return {
            'length': len(self.show),
            'height': self.formatting.height,
        }


class Cell(DocxPart):
    """Cell object."""

    tag = 'tc'

    def __init__(self, xml_element: ElementTree):
        """
        Create a table cell instance.

        Args:
            xml_element: cell xml
        """
        super().__init__(
            xml_element=xml_element,
            formatting=CellFormat,
            nodes=(Paragraph, Table),
        )

    @property
    def paragraphs(self) -> list[Paragraph]:
        """Get Cell Paragraphs getter."""

        return [node for node in self._nodes if isinstance(node, Paragraph)]

    @property
    def tables(self) -> list[Table]:
        """Get Cell tables."""

        return [node for node in self._nodes if isinstance(node, Table)]

    @property
    def text(self) -> str:
        """Get cell text."""

        return '\n'.join([part.text for part in self._nodes])

    @property
    def show(self) -> list:
        """Show structure text."""
        return [part.show for part in self._nodes]

    @property
    def properties(self) -> dict[str, int]:
        """Get Cell properties."""

        return {
            'h_merge': self.formatting.h_merge,
            'v_merge': self.formatting.v_merge,
        }
