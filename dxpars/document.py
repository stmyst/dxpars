"""Docx Document."""

from pathlib import Path
from typing import Any, IO, Optional, Union
from xml.etree import ElementTree
from zipfile import ZipFile

from dxpars.docx_objects.body import Body
from dxpars.docx_objects.paragraph import Paragraph
from dxpars.docx_objects.table import Table


class Document(object):
    """Parsed docx document."""

    def __init__(
        self, file_or_path: Union[str, IO], filename: Optional[str] = None,
    ) -> None:
        """
        Docx Document instance.

        Args:
            file_or_path: file or path to file
            filename: filename (for IO)
        """
        self.filename = self._get_filename(path=file_or_path, filename=filename)
        with ZipFile(file_or_path) as zipf:
            self.body = Body(doc_tree=ElementTree.fromstring(zipf.read('word/document.xml')))

    def __str__(self) -> str:
        """
        Document name.

        Returns:
            docx_document filename
        """
        return f'{self.filename} at {id(self)}'

    __repr__ = __str__

    @property
    def text(self) -> str:
        """
        Get document text.

        Returns:
            Document text.
        """
        return self.body.text

    @property
    def parts(self) -> list:
        """
        Get all parts of the document.

        Returns:
            List of Paragraph and Table objects.
        """
        return self.body.parts

    @property
    def paragraphs(self) -> list[Paragraph]:
        """
        Get paragraphs.

        Returns:
            Document paragraphs.
        """
        return self.body.paragraphs

    @property
    def tables(self) -> list[Table]:
        """
        Get tables.

        Returns:
            Document tables.
        """
        return self.body.tables

    @property
    def to_dict(self) -> dict[str, Any]:
        """
        Get dictionary representation of the document.

        Returns:
            Dictionary with document data.
        """
        return {'name': self.filename, 'body': self.body.to_dict}

    def to_txt(
        self,
        folder: str,
        filename: Optional[str] = None,
        mode: str = 'w',
        encoding: str = 'utf-8',
    ):
        if filename is None:
            filename = '{name}.txt'.format(name=self.filename.split('.')[0])
        folder = Path(folder) / filename
        with open(folder, mode=mode, encoding=encoding) as file:
            for part in self.body.parts:
                file.write(f'{part.text}\n')

    def _get_filename(self, path: Union[str, IO], filename: Optional[str]) -> str:
        """
        Get docx_document filename.

        Args:
            filename: filename
            path: path to file

        Returns:
            Document filename
        """
        if isinstance(path, str):
            return path
        return self.__class__.__name__ if filename is None else filename
