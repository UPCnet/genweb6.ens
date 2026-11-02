# -*- coding: utf-8 -*-

from plone.app.dexterity import textindexer
from plone.dexterity.interfaces import IDexteritySchema
from plone.supermodel import model
from zope import schema

from genweb6.ens import _


try:
    from plone.app.dexterity.config import MAX_DESCRIPTION_LENGTH
    from plone.app.dexterity.config import MAX_TITLE_LENGTH
except ImportError:  # plone.app.dexterity < 3.2.3
    MAX_TITLE_LENGTH = 1024
    MAX_DESCRIPTION_LENGTH = 10000


class IPersona(model.Schema, IDexteritySchema):
    """
    Persona amb un càrrec
    """

    textindexer.searchable('title')
    title = schema.TextLine(
        max_length=MAX_TITLE_LENGTH,
        title=_(u"Cognoms i nom"),
        description=_(u"Escriu amb el format: Cognoms, Nom"),
        required=True
    )

    textindexer.searchable('dni')
    dni = schema.TextLine(
        title=_(u"DNI"),
        required=False)

    textindexer.searchable('carrec')
    carrec = schema.TextLine(
        title=_(u"Carrec"),
        required=False
    )
