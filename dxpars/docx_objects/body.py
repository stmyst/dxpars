from xml.etree import ElementTree

from dxpars.base.base_objects import DocxPart
from dxpars.docx_objects.paragraph import Paragraph
from dxpars.docx_objects.table import Table
from dxpars.format.paragraph import BodyFormat


class Body(DocxPart):
    """Docx docx_document body object."""

    tag = 'body'

    def __init__(self, doc_tree: ElementTree):
        """
        Create a body instance.

        Args:
            doc_tree: docx_document xml tree
        """
        super().__init__(
            xml_element=doc_tree.find(self._make_tag(tag=self.tag)),
            formatting=BodyFormat,
            nodes=(Paragraph, Table),
        )

    @property
    def text(self) -> str:
        """Get Document text."""

        return '\n'.join([part.text for part in self._nodes])

    @property
    def show(self) -> list:
        return [part.show for part in self._nodes]

    @property
    def paragraphs(self) -> list[Paragraph]:
        """Get Document paragraphs."""

        return [node for node in self._nodes if isinstance(node, Paragraph)]

    @property
    def tables(self) -> list[Table]:
        """Get Document tables."""

        return [node for node in self._nodes if isinstance(node, Table)]

    @property
    def properties(self):
        """Get body properties."""

        return None
