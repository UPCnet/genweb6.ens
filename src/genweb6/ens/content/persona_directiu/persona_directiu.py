# -*- coding: utf-8 -*-

from plone.dexterity.content import Container
from zope import schema
from zope.interface import implementer

from genweb6.ens import _
from genweb6.ens.content.persona_contacte.persona_contacte import IPersonaContacte


class IPersonaDirectiu(IPersonaContacte):
    description = schema.Text(
        title=_(u"Descripció"),
        required=False)

    is_historic = schema.Bool(
        title=_(u"Històric"),
        defaultFactory=lambda: False,
        required=False)


@implementer(IPersonaDirectiu)
class PersonaDirectiu(Container):

    @property
    def b_icon_expr(self):
        return "person"