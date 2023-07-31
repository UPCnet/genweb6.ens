# -*- coding: utf-8 -*-

from plone.app.dexterity import textindexer
from plone.dexterity.content import Container
from zope import schema
from zope.interface import implementer

from genweb6.ens import _
from genweb6.ens.content.document_legal.document_legal import IDocumentLegal


class IEscripturaPublica(IDocumentLegal):
    """
    Escriptura pública associada a un ens.
    """

    textindexer.searchable('notari')
    notari = schema.TextLine(
        title=_(u"Notari"),
        required=False,
    )


@implementer(IEscripturaPublica)
class EscripturaPublica(Container):

    @property
    def b_icon_expr(self):
        return "file-text"