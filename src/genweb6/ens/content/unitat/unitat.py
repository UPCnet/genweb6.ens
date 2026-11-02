# -*- coding: utf-8 -*-

from plone.app.dexterity import textindexer
from plone.dexterity.content import Container
from plone.dexterity.interfaces import IDexteritySchema
from plone.supermodel import model
from zope import schema
from zope.interface import implementer

from genweb6.ens import _


try:
    from plone.app.dexterity.config import MAX_DESCRIPTION_LENGTH
    from plone.app.dexterity.config import MAX_TITLE_LENGTH
except ImportError:  # plone.app.dexterity < 3.2.3
    MAX_TITLE_LENGTH = 1024
    MAX_DESCRIPTION_LENGTH = 10000


class IUnitat(model.Schema, IDexteritySchema):
    """
    Unitat de la UPC.
    """

    textindexer.searchable('title')
    title = schema.TextLine(
        max_length=MAX_TITLE_LENGTH,
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