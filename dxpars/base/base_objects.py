"""Docx xml objects"""

from abc import ABC, abstractmethod
from typing import Any, Generator, Optional
from xml.etree import ElementTree


class XmlElement(object):
    """XML docx_document part."""

    namespace: str = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
    tag: str

    def __init__(self, xml_element: ElementTree):
        """
        XmlElement instance.

        Args:
            xml_element: xml tree

        """
        self._xml = xml_element

    @property
    def show_xml(self) -> Optional[list[str]]:
        """Show XML representation of the element."""

        if self._xml is not None:
            ElementTree.indent(self._xml)
            return ElementTree.tostring(self._xml, encoding='unicode', method="xml").splitlines()
        return None

    def _make_tag(self, tag: str) -> str:
        return f'{self.namespace}{tag}'


class DocxPart(ABC, XmlElement):
    """Doc object."""

    def __init__(self, xml_element: ElementTree, formatting, nodes=None):
        """
        Create Document object instance.

        Args:
            xml_element: xml tree
            formatting: xml with formatting
            nodes: list of nodes to parse

        """
        super().__init__(xml_element=xml_element)
        self._nodes = [] if nodes is None else list(self._cut_nodes(nodes=nodes))
        self.formatting = next(
            self._cut_nodes(nodes=(formatting, )), formatting(xml_element=None),
        )

    def __str__(self) -> str:
        """Object representation."""

        return f'{self.__class__.__name__} at {id(self)}'

    __repr__ = __str__

    @abstractmethod
    def text(self) -> str:
        """Returns object text."""

    @abstractmethod
    def properties(self) -> Optional[dict]:
        """Returns main properties."""

    @abstractmethod
    def show(self):
        """Returns object structure."""

    @property
    def parts(self):
        """Get child nodes or text of the object."""

        return self._nodes or self.text

    @property
    def to_dict(self) -> dict[str, Any]:
        """Get dictionary representation of the object."""

        return {
            'object': self.__class__.__name__,
            'properties': self.properties,
            'parts': {
                idx: part.to_dict for idx, part in enumerate(self._nodes)
            } if self._nodes else self.text,
        }

    def _cut_nodes(self, nodes) -> Generator:
        nodes = {self._make_tag(tag=node.tag): node for node in nodes}
        for xml_node in self._xml:
            node_object = nodes.get(xml_node.tag)
            if node_object is not None:
                yield node_object(xml_element=xml_node)


class FormatElement(XmlElement):
    """Doc object format."""

    def __init__(self, xml_element: ElementTree):
        """
        Create Format object instance.

        Args:
            xml_element: xml tree
        """
        super().__init__(xml_element=xml_element)
        self.properties = self._extract_tags_data(element=self._xml)

    @classmethod
    def extract_tag(cls, node: str) -> str:
        """
        Get tag.

        Args:
            node: xml node
        """
        return node.split('}')[1]

    def get_tag_value(
        self, tag: str, tag_value_key: str = 'val', default=None,
    ) -> Any:
        """
        Get tag value.

        Args:
            tag: tag
            tag_value_key: tag value key
            default: default value, if not tag data
        """
        tag_data = self.properties.get(tag)
        if tag_data is None or not tag_data:
            return default
        tag_value = tag_data.get(tag_value_key)
        return int(tag_value) if tag_value.isdigit() else tag_value

    def _extract_tags_data(self, element: ElementTree) -> dict[str, Any]:
        tags_data = {}
        if element is not None:
            for node in element:
                tag = self.extract_tag(node=node.tag)
                if list(node):
                    tags_data[tag] = self._extract_tags_data(element=node)
                else:
                    tags_data[tag] = {
                        self.extract_tag(tag): tag_value
                        for tag, tag_value in node.attrib.items()
                    }
        return tags_data
