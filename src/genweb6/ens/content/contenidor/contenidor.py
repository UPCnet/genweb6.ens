# -*- coding: utf-8 -*-

from plone.app.dexterity import textindexer
from plone.supermodel import model
from zope import schema

from genweb6.ens import _


class IContenidor(model.Schema):
    textindexer.searchable('title')
    title = schema.TextLine(
        title=_(u"Nom"),
        required=True)

    textindexer.searchable('description')
    description = schema.Text(
        title=_(u"Descripció"),
        required=False)
