# -*- coding: utf-8 -*-

from plone.app.dexterity import textindexer
from plone.dexterity.interfaces import IDexteritySchema
from plone.namedfile.field import NamedBlobFile
from plone.supermodel import model
from zope import schema

from genweb6.ens import _


class IDocumentLegal(model.Schema, IDexteritySchema):
    """
    Document legal
    """

    textindexer.searchable('title')
    title = schema.TextLine(
        title=_(u"Títol"),
        required=True
    )

    textindexer.searchable('description')
    description = schema.Text(
        title=_(u"Descripció"),
        required=False)

    data = schema.Date(
        title=_(u"Data"),
        required=False)

    fitxer = NamedBlobFile(
        title=_(u"Fitxer"),
        description=_(u"Puja un fitxer"),
        required=False)
