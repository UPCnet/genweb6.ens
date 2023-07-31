# -*- coding: utf-8 -*-

from plone.app.dexterity import textindexer
from plone.dexterity.content import Container
from zope import schema
from zope.interface import implementer

from genweb6.ens import _
from genweb6.ens.content.persona.persona import IPersona


class IPersonaContacte(IPersona):
    """
    Persona amb un càrrec i dades de contacte
    """

    textindexer.searchable('telefon')
    telefon = schema.TextLine(
        title=_(u"Telèfon"),
        required=False
    )

    # TODO Validate email
    textindexer.searchable('email')
    email = schema.TextLine(
        title=_(u"Email"),
        required=False
    )


@implementer(IPersonaContacte)
class PersonaContacte(Container):

    @property
    def b_icon_expr(self):
        return "person"