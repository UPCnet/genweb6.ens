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


class IContenidor(model.Schema, IDexteritySchema):
    textindexer.searchable('title')
    title = schema.TextLine(
        max_length=MAX_TITLE_LENGTH,
        title=_(u"Nom"),
        required=True)

    textindexer.searchable('description')
    description = schema.Text(
        max_length=MAX_DESCRIPTION_LENGTH,
        title=_(u"Descripció"),
        required=False)
