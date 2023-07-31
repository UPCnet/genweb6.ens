# -*- coding: utf-8 -*-

from plone.app.dexterity import textindexer
from plone.dexterity.content import Container
from plone.supermodel import model
from zope import schema
from zope.interface import implementer
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary

from genweb6.ens import _


def get_vocabulary(values):
    return SimpleVocabulary([
        SimpleTerm(title=_(value), value=value, token=token)
        for token, value in enumerate(values)])


class IOrgan(model.Schema):
    """
    Òrgan de govern associat a un ens.
    """

    textindexer.searchable('title')
    title = schema.TextLine(
        title=_(u"Nom"),
        required=True
    )

    textindexer.searchable('description')
    description = schema.Text(
        title=_(u"Descripció"),
        required=False)

    textindexer.searchable('composicio')
    composicio = schema.Text(
        title=_(u"Composició"),
        required=False)

    tipus = schema.Choice(
        title=_(u"Tipus"),
        vocabulary=get_vocabulary([
            u"Govern",
            u"Assessor"]),
        required=True)

    is_historic = schema.Bool(
        title=_(u"Històric"),
        defaultFactory=lambda: False,
        required=False)


@implementer(IOrgan)
class Organ(Container):

    @property
    def b_icon_expr(self):
        return "journals"