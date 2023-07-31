# -*- coding: utf-8 -*-

from plone.app.dexterity import textindexer
from plone.dexterity.content import Container
from zope import schema
from zope.interface import implementer

from genweb6.ens import _
from genweb6.ens.content.document_legal.document_legal import IDocumentLegal


class IAcord(IDocumentLegal):
    """
    Acord legal associt a un òrgan de govern.
    """
    textindexer.searchable('organ')
    organ = schema.TextLine(
        title=_(u"Òrgan"),
        required=False
    )


@implementer(IAcord)
class Acord(Container):

    @property
    def b_icon_expr(self):
        return "file-text"