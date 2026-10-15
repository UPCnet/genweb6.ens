# -*- coding: utf-8 -*-

from plone.app.dexterity import textindexer
from plone.dexterity.content import Container
from plone.dexterity.interfaces import IDexteritySchema
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


try:
    from plone.app.dexterity.config import MAX_DESCRIPTION_LENGTH
    from plone.app.dexterity.config import MAX_TITLE_LENGTH
except ImportError:  # plone.app.dexterity < 3.2.3
    MAX_TITLE_LENGTH = 1024
    MAX_DESCRIPTION_LENGTH = 10000


class IOrgan(model.Schema, IDexteritySchema):
    """
    Òrgan de govern associat a un ens.
    """

    textindexer.searchable('title')
    title = schema.TextLine(
        max_length=MAX_TITLE_LENGTH,
        title=_(u"Nom"),
        required=True
    )

    textindexer.searchable('description')
    description = schema.Text(
        max_length=MAX_DESCRIPTION_LENGTH,
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