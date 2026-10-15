# -*- coding: utf-8 -*-

from plone.app.dexterity import textindexer
from plone.dexterity.content import Container
from plone.dexterity.interfaces import IDexteritySchema
from plone.supermodel import model
from zope import schema
from zope.interface import implementer

from genweb6.ens import _


try:
    from plone.app.dexterity.config import MAX_DESCRIPTION_LENGTH
    from plone.app.dexterity.config import MAX_TITLE_LENGTH
except ImportError:  # plone.app.dexterity < 3.2.3
    MAX_TITLE_LENGTH = 1024
    MAX_DESCRIPTION_LENGTH = 10000


class ICarrec(model.Schema, IDexteritySchema):
    """
    Càrrec associat a un òrgan d'un ens.
    """

    textindexer.searchable('ens')
    ens = schema.TextLine(
        title=_(u"Ens"),
        required=True)

    textindexer.searchable('title')
    title = schema.TextLine(
        max_length=MAX_TITLE_LENGTH,
        title=_(u"Cognoms i nom"),
        required=True)

    textindexer.searchable('carrec_envirtud')
    carrec_envirtud = schema.TextLine(
        title=_(u"En virtud del seu càrrec de:"),
        required=False)

    textindexer.searchable('carrec')
    carrec = schema.TextLine(
        title=_(u"Càrrec a l'entitat"),
        required=True)

    data_inici = schema.Date(
        title=_(u"Data d'inici"),
        required=False)

    vigencia = schema.TextLine(
        title=_(u"Vigència"),
        required=False)

    data_fi = schema.Date(
        title=_(u"Data de fi"),
        required=False)

    is_historic = schema.Bool(
        title=_(u"Històric"),
        defaultFactory=lambda: False,
        required=False)

    nomenaments_anteriors = schema.Text(
        title=_(u"Nomenaments anteriors"),
        required=False)

    observacions = schema.Text(
        title=_(u"Observacions"),
        required=False)


@implementer(ICarrec)
class Carrec(Container):

    @property
    def b_icon_expr(self):
        return "person"