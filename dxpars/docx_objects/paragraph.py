"""docx Paragraph docx_objects."""

from typing import Optional, Union
from xml.etree import ElementTree

from dxpars.base.base_objects import DocxPart
from dxpars.format.paragraph import ParagraphFormat, RunFormat


class Paragraph(DocxPart):
    """Paragraph object."""

    tag = 'p'

    def __init__(self, xml_element: ElementTree) -> None:
        """
        Create a paragraph instance.

        Args:
            xml_element: docx Paragraph
        """
        super().__init__(
            xml_element=xml_element, formatting=ParagraphFormat, nodes=(Run,),
        )

    @property
    def text(self) -> str:
        """Get paragraph text."""

        return ''.join(run.text for run in self._nodes)

    @property
    def show(self):
        return self.text

    @property
    def bold(self) -> bool:
        """Get bold format."""

        if not self._nodes:
            return self.formatting.has_run_with_format(tag='b')
        bold_condition = (
            run.bold
            for run in self._nodes
            if all([run.text, run.text not in ['\n', '\t']])
        )
        return all(bold_condition)

    @property
    def italic(self) -> bool:
        """Get Italic format."""

        if not self._nodes:
            return self.formatting.has_run_with_format(tag='i')
        return all(run.italic for run in self._nodes)

    @property
    def underline(self) -> bool:
        """Get Underline format."""
        if not self._nodes:
            return self.formatting.has_run_with_format(tag='u')
        return all(run.underline for run in self._nodes)

    @property
    def caps(self) -> bool:
        """Get Caps format."""

        return any(
            [
                self.text.isupper(),
                self._nodes and all(run.caps for run in self._nodes),
            ],
        )

    @property
    def bullet(self) -> bool:
        """Get Bullet format."""

        return self.formatting.properties.get('numPr') is not None

    @property
    def alignment(self) -> str:
        """Get Alignment."""

        return self.formatting.get_tag_value(tag='jc', default='left')

    @property
    def pstyle(self) -> Optional[str]:
        """Get Paragraph style."""

        return self.formatting.get_tag_value(tag='pStyle')


    @property
    def properties(self) -> dict[str, Union[str, bool]]:
        """Get Paragraph properties."""

        return {
            'alignment': self.alignment,
            'bold': self.bold,
            'italic': self.italic,
            'underline': self.underline,
            'pstyle': self.pstyle,
            'caps': self.caps,
            'bullet': self.bullet,
        }


class Run(DocxPart):
    """Run object."""

    tag = 'r'

    def __init__(self, xml_element: ElementTree):
        """
        Create a paragraph Run instance.

        Args:
            xml_element: Run xml
        """
        super().__init__(xml_element=xml_element, formatting=RunFormat)

    @property
    def text(self) -> str:
        """Get Run text."""

        idents = {
            f'{self.namespace}tab': '\t',
            f'{self.namespace}br': '\n',
            f'{self.namespace}t': 't',
        }

        text = []
        for node in self._xml:
            ident = idents.get(node.tag)
            if ident is not None:
                if ident == 't' and node.text is not None:
                    text.append(node.text)
                else:
                    text.append(ident)
        return ''.join(text)

    @property
    def show(self) -> str:
        """Get Run text."""
        return self.text

    @property
    def bold(self) -> bool:
        """Get Bold."""

        return self._has_run_property(tag='b')

    @property
    def italic(self) -> bool:
        """Get Italic."""
        return self._has_run_property(tag='i')

    @property
    def underline(self) -> bool:
        """Get Underline."""

        return self.formatting.properties.get('u') is not None

    @property
    def caps(self) -> bool:
        """Get Caps."""

        return self.formatting.properties.get('caps') is not None

    @property
    def properties(self) -> dict[str, bool]:
        """Get Run properties."""

        return {
            'bold': self.bold,
            'italic': self.italic,
            'underline': self.underline,
            'caps': self.caps,
        }

    def _has_run_property(self, tag: str) -> bool:
        prop = self.formatting.properties.get(tag)
        if prop is None:
            return False
        if not prop:
            return True
        return prop['val'].isdigit() and int(prop['val']) > 0