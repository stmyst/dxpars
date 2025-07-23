from typing import Optional
from xml.etree import ElementTree

from dxpars.base.base_objects import FormatElement


class BodyFormat(FormatElement):
    """Body formatting object."""

    tag = 'sectPr'

    def __init__(self, xml_element: ElementTree):
        """
        Create a BodyFormat instance.

        Args:
            xml_element: mxl with formatting
        """
        super().__init__(xml_element=xml_element)


class ParagraphFormat(FormatElement):
    """Paragraph formatting object."""

    tag = 'pPr'

    def __init__(self, xml_element: ElementTree):
        """
        Create a ParagraphFormat instance.

        Args:
            xml_element: mxl with formatting
        """
        super().__init__(xml_element=xml_element)


    @property
    def spacing(self) -> Optional[dict]:
        """Get Spacing format getter."""

        return self.properties.get('spacing')

    def has_run_with_format(self, tag: str) -> bool:
        """
        Find Run format by tag.

        Args:
            tag: run tag
        """
        run_prop = self.properties.get('rPr')
        return run_prop is not None and run_prop.get(tag) is not None


class RunFormat(FormatElement):
    """Run formatting object."""

    tag = 'rPr'

    def __init__(self, xml_element):
        """
        Create a ParagraphFormat instance.

        Args:
            xml_element: mxl with formatting
        """
        super().__init__(xml_element=xml_element)
