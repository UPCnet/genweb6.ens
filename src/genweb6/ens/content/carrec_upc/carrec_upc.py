# -*- coding: utf-8 -*-

from plone.app.dexterity import textindexer
from plone.autoform import directives
from plone.dexterity.content import Container
from zope import schema
from zope.component.hooks import getSite
from zope.interface import Invalid
from zope.interface import directlyProvides
from zope.interface import implementer
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary

from genweb6.ens import _
from genweb6.ens.content.carrec.carrec import ICarrec
from genweb6.ens.data_access.carrec import CarrecDataReporter


def prettify_representant(representant):
    return representant.Title.decode('utf-8') + ' - ' + representant.carrec


def get_vocabulary_representants_upc(context):
    catalog = getSite().portal_catalog
    reporter = CarrecDataReporter(catalog)

    vocabulary_terms = []

    # Get representants from Persones
    vocabulary_terms.append(SimpleTerm(
        title="Persones:",
        value="persones",
        token="persones"))
    vocabulary_terms += [
        SimpleTerm(title=" - " + prettify_representant(
                   representant).encode('utf-8'),
                   value=prettify_representant(representant),
                   token=representant.id)
        for representant in reporter.list_representants('persones')]

    return SimpleVocabulary(vocabulary_terms)


directlyProvides(get_vocabulary_representants_upc, IContextSourceBinder)


def title_constraint(value):
    if value == ("consell-de-direccio", "altres", "persones"):
        raise Invalid(_(u"Cal que introduïu cognoms i nom"))
    return True


class ICarrecUPC(ICarrec):
    """
    Càrrec associat a un òrgan d'UPC.
    """

    textindexer.searchable('ens')
    ens = schema.TextLine(
        title=_(u"Ens"),
        defaultFactory=lambda: u"UPC",
        readonly=True,
        required=True)

    directives.order_before(title='*')
    textindexer.searchable('title')
    title = schema.Choice(
        title=_(u"Cognoms i nom"),
        source=get_vocabulary_representants_upc,
        required=True,
        constraint=title_constraint)


@implementer(ICarrecUPC)
class CarrecUPC(Container):

    @property
    def b_icon_expr(self):
        return "person"