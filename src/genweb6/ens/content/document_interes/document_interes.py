# -*- coding: utf-8 -*-

from zope.interface import implementer
from plone.dexterity.content import Container

from genweb6.ens.content.document_legal.document_legal import IDocumentLegal


class IDocumentInteres(IDocumentLegal):
    """
    Document d'interès legal
    """
    pass


@implementer(IDocumentInteres)
class DocumentInteres(Container):

    @property
    def b_icon_expr(self):
        return "file-text"