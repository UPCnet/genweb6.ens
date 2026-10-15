# -*- coding: utf-8 -*-

from plone.dexterity.content import Container
from zope import schema
from zope.interface import implementer

from genweb6.ens import _
from genweb6.ens.content.persona_contacte.persona_contacte import IPersonaContacte


try:
    from plone.app.dexterity.config import MAX_DESCRIPTION_LENGTH
    from plone.app.dexterity.config import MAX_TITLE_LENGTH
except ImportError:  # plone.app.dexterity < 3.2.3
    MAX_TITLE_LENGTH = 1024
    MAX_DESCRIPTION_LENGTH = 10000


class IPersonaDirectiu(IPersonaContacte):
    description = schema.Text(
        max_length=MAX_DESCRIPTION_LENGTH,
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