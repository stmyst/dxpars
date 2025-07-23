from xml.etree import ElementTree

from dxpars.base.base_objects import FormatElement


class TableFormat(FormatElement):
    """Table formatting object."""

    tag = 'tblPr'

    def __init__(self, xml_element: ElementTree):
        """
        Create a TableFormat instance.

        Args:
            xml_element: mxl with formatting
        """
        super().__init__(xml_element=xml_element)


class RowFormat(FormatElement):
    """Row formatting object."""

    tag = 'trPr'

    def __init__(self, xml_element: ElementTree):
        """
        Create a RowFormat instance.

        Args:
            xml_element: mxl with formatting
        """
        super().__init__(xml_element=xml_element)

    @property
    def height(self):
        """Get Row height ."""

        return self.get_tag_value(tag='trHeight')


class CellFormat(FormatElement):
    """Row formatting object."""

    tag = 'tcPr'

    def __init__(self, xml_element: ElementTree):
        """
       Create a CellFormat instance.

       Args:
           xml_element: mxl with formatting
       """
        super().__init__(xml_element=xml_element)

    @property
    def h_merge(self) -> int:
        """Get number of horizontally merged cells."""

        return self.get_tag_value(tag='gridSpan', default=1)

    @property
    def v_merge(self) -> dict:
        """Get vertical merging data."""
        merged, first = False, False
        if self._xml is not None:
            v_merge = self._xml.find(path=self._make_tag(tag='vMerge'))
            merged = v_merge is not None
            first = merged and 'restart' in v_merge.attrib.values()
        return {'merged': merged, 'first': first}