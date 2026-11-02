# -*- coding: utf-8 -*-

from plone.app.dexterity import textindexer
from plone.dexterity.interfaces import IDexteritySchema
from plone.namedfile.field import NamedBlobFile
from plone.supermodel import model
from zope import schema

from genweb6.ens import _


try:
    from plone.app.dexterity.config import MAX_DESCRIPTION_LENGTH
    from plone.app.dexterity.config import MAX_TITLE_LENGTH
except ImportError:  # plone.app.dexterity < 3.2.3
    MAX_TITLE_LENGTH = 1024
    MAX_DESCRIPTION_LENGTH = 10000


class IDocumentLegal(model.Schema, IDexteritySchema):
    """
    Document legal
    """

    textindexer.searchable('title')
    title = schema.TextLine(
        max_length=MAX_TITLE_LENGTH,
        title=_(u"Títol"),
        required=True
    )

    textindexer.searchable('description')
    description = schema.Text(
        max_length=MAX_DESCRIPTION_LENGTH,
        title=_(u"Descripció"),
        required=False)

    data = schema.Date(
        title=_(u"Data"),
        required=False)

    fitxer = NamedBlobFile(
        title=_(u"Fitxer"),
        description=_(u"Puja un fitxer"),
        required=False)
