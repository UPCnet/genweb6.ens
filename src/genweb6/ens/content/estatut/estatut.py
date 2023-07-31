# -*- coding: utf-8 -*-

from plone.dexterity.content import Container
from zope import schema
from zope.interface import implementer

from genweb6.ens import _
from genweb6.ens.content.document_legal.document_legal import IDocumentLegal


class IEstatut(IDocumentLegal):
    """
    Estatut associat a un ens.
    """

    is_vigent = schema.Bool(
        title=_(u"Vigent"),
        defaultFactory=lambda: True,
        required=False,
    )


@implementer(IEstatut)
class Estatut(Container):

    @property
    def b_icon_expr(self):
        return "file-text"