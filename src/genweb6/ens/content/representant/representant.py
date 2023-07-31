# -*- coding: utf-8 -*-

from plone.app.dexterity import textindexer
from plone.dexterity.content import Container
from zope import schema
from zope.interface import implementer
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary

from genweb6.ens import _
from genweb6.ens.content.persona.persona import IPersona


carrecs = [
    u"PDI",
    u"PAS",
    u"Estudiant",
    u"Extern",
    u"Extern CS"]


class IRepresentant(IPersona):
    """
    Càrrec que pot representar UPC en algun ens
    """

    def get_vocabulary(values):
        return SimpleVocabulary([
            SimpleTerm(title=_(value), value=value, token=token)
            for token, value in enumerate(values)])

    textindexer.searchable('carrec')
    carrec = schema.Choice(
        title=_(u"Col·lectiu"),
        vocabulary=get_vocabulary(carrecs),
        required=False
    )


@implementer(IRepresentant)
class Representant(Container):

    @property
    def b_icon_expr(self):
        return "person"