# -*- coding: utf-8 -*-

from plone.app.dexterity import textindexer
from plone.dexterity.content import Container
from plone.supermodel import model
from zope import schema
from zope.interface import implementer

from genweb6.ens import _


class IUnitat(model.Schema):
    """
    Unitat de la UPC.
    """

    textindexer.searchable('title')
    title = schema.TextLine(
        title=_(u"Nom"),
        required=True
    )

    textindexer.searchable('persona')
    persona = schema.TextLine(
        title=_(u"Persona de referència"),
        required=False)

    textindexer.searchable('observacions')
    observacions = schema.TextLine(
        title=_(u"Observacions"),
        required=False)


@implementer(IUnitat)
class Unitat(Container):

    @property
    def b_icon_expr(self):
        return "building"