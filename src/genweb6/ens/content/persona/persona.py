# -*- coding: utf-8 -*-

from plone.app.dexterity import textindexer
from plone.dexterity.interfaces import IDexteritySchema
from plone.supermodel import model
from zope import schema

from genweb6.ens import _


class IPersona(model.Schema, IDexteritySchema):
    """
    Persona amb un càrrec
    """

    textindexer.searchable('title')
    title = schema.TextLine(
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
