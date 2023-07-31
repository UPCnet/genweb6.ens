# -*- coding: utf-8 -*-

from Products.Five.browser import BrowserView

from plone import api
from plone.app.dexterity import textindexer
from plone.autoform import directives
from plone.dexterity.content import Container
from plone.dexterity.content import Item
from plone.supermodel import model
from z3c.form.browser.radio import RadioFieldWidget
from zope import schema
from zope.interface import implementer
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary

from genweb6.ens import _
from genweb6.ens.data_access.ens import EnsDataReporter


figura_juridica_values = [
    u"Fundació",
    u"Societat",
    u"Consorci",
    u"Associació",
    u"Sense NIF",
    u"Altra"]

estat_values = [
    _(u"Actiu"),
    u"Pre-Baixa",
    u"Pre-Alta",
    u"Baixa",
    u"Pre-Alta cancel·lada",
    u"Altre"]

institution_type_values = [
    _(u"Estatal"),
    _(u"Autonòmica"),
    u"Local",
    u"Internacional",
    u"Altres CCAA"]


class IEns(model.Schema):
    """
    Organització com ara una universitat o una empresa.
    """

    def get_vocabulary(values):
        return SimpleVocabulary([
            SimpleTerm(title=_(value), value=value, token=token)
            for token, value in enumerate(values)])

    model.fieldset(
        "dades_identificatives",
        label=u"Dades identificatives",
        fields=['title', 'acronim', 'description', 'objecte_social',
                'estat', 'nif', 'institution_type', 'figura_juridica',
                'numero_identificacio', 'domicili_social_poblacio',
                'domicili_social_adreca', 'adreca_2', 'telefon', 'fax',
                'web', 'tipologia_upc', 'codi', 'num_ens', 'etiquetes',
                'dades_identificatives_observacions'])

    textindexer.searchable('title')
    title = schema.TextLine(
        title=_(u"Denominació completa"),
        required=True
    )

    textindexer.searchable('acronim')
    acronim = schema.TextLine(
        title=_(u"Acrònim"),
        required=True,
    )

    textindexer.searchable('description')
    description = schema.Text(
        title=_(u"Descripció"),
        required=False)

    textindexer.searchable('objecte_social')
    objecte_social = schema.Text(
        title=_(u"Objecte social"),
        required=False)

    textindexer.searchable('estat')
    estat = schema.Choice(
        title=_(u"Estat"),
        vocabulary=get_vocabulary(estat_values),
        required=True)

    textindexer.searchable('nif')
    nif = schema.TextLine(
        title=_(u"NIF"),
        required=False,
    )

    institution_type = schema.Choice(
        title=_(u"Àmbit institucional"),
        vocabulary=get_vocabulary(institution_type_values),
        required=True)

    figura_juridica = schema.Choice(
        title=_(u"Figura jurídica"),
        vocabulary=get_vocabulary(figura_juridica_values),
        default="Altra",
        required=True)

    textindexer.searchable('numero_identificacio')
    numero_identificacio = schema.TextLine(
        title=_(u"Número d'identificació"),
        required=False)

    textindexer.searchable('domicili_social_poblacio')
    domicili_social_poblacio = schema.TextLine(
        title=_(u"Domicili social (població)"),
        required=False)

    textindexer.searchable('domicili_social_adreca')
    domicili_social_adreca = schema.TextLine(
        title=_(u"Domicili social (adreça)"),
        required=False)

    textindexer.searchable('adreca_2')
    adreca_2 = schema.TextLine(
        title=_(u"Adreça 2"),
        required=False)

    textindexer.searchable('telefon')
    telefon = schema.TextLine(
        title=_(u"Telèfon"),
        required=False)

    textindexer.searchable('fax')
    fax = schema.TextLine(
        title=_(u"Fax"),
        required=False)

    textindexer.searchable('web')
    web = schema.TextLine(
        title=_(u"Web"),
        required=False)

    tipologia_upc = schema.Choice(
        title=_(u"Tipologia UPC"),
        vocabulary=get_vocabulary([
            u"-",
            u"Grup UPC",
            u"Participació Superior",
            u"Entitat Vinculada de Recerca",
            u"Centre Docent",
            u"Institut de Recerca",
            u"Spin-off",
            u"Internacional",
            u"Patronats i Consells Assessors",
            u"Institut de Ciències de l’Educació",
            u"Centres de Recerca",
            u"Departaments",
            u"Grups de Recerca",
            u"Escola de Doctorat",
            u"Càtedres",
            u"Instituts Universitaris de Recerca vinculats",
            u"Centres Docents Adscrits",
            u"Unitats d’Administració i Serveis",
            u"Altra"]),
        required=True)

    textindexer.searchable('codi')
    codi = schema.TextLine(
        title=_(u"Codi UPC"),
        required=False)

    textindexer.searchable('num_ens')
    num_ens = schema.Int(
        title=_(u"Núm."),
        required=False)

    # Campo oculto porque se usaran las etiquetas estandar de plone
    textindexer.searchable('etiquetes')
    directives.omitted('etiquetes')
    etiquetes = schema.Text(
        title=_(u"Etiquetes"),
        required=False)

    textindexer.searchable('dades_identificatives_observacions')
    dades_identificatives_observacions = schema.Text(
        title=_(u"Observacions"),
        required=False)

    model.fieldset(
        "participacio",
        label=u"Participació de la UPC",
        fields=['title1',
                'participacio_data',
                'capital_social_sn', 'capital_social_import', 'capital_social_moneda',
                'aportacio_total', 'aportacio_total_moneda',
                'aportacio_sn', 'aportacio_import', 'aportacio_moneda',
                'percentatge_participacio',
                'unitat_carrec',
                'participacio_observacions',
                'title2',
                'total_membres',
                'nombre_membres',
                'percentatge_membres',
                'membres_observacions',
                'title3',
                'quota_sn', 'quota_import', 'quota_moneda', 'quota_observacions']
    )

    directives.mode(title1='display')
    title1 = schema.TextLine(
        title=_(u""),
        default=_(u"1. Al capital social o fons patrimonial"),
    )

    directives.widget(aportacio_sn=RadioFieldWidget)
    directives.omitted('aportacio_sn')
    aportacio_sn = schema.Choice(
        title=_(u"Import UPC"),
        vocabulary=SimpleVocabulary(
            [SimpleTerm(title=_(u"Sí"), value=True),
             SimpleTerm(title=_(u"No"), value=False),
             SimpleTerm(title=_(u"Desconeguda"), value=None)]),
        required=False,
    )

    aportacio_import = schema.Float(
        title=_(u"Aportació inicial UPC"),
        required=False)

    participacio_data = schema.Date(
        title=_(u"Data"),
        required=False)

    aportacio_moneda = schema.TextLine(
        title=_(u"Moneda"),
        required=False)

    aportacio_total = schema.Float(
        title=_(u"Capital inicial total"),
        required=False)

    aportacio_total_moneda = schema.TextLine(
        title=_(u"Moneda"),
        required=False)

    directives.mode(title3='display')
    title3 = schema.TextLine(
        title=_(u""),
        default=_(u"3. Quota anual"),
    )

    directives.widget(quota_sn=RadioFieldWidget)
    directives.omitted('quota_sn')
    quota_sn = schema.Choice(
        title=_(u"Quota"),
        vocabulary=SimpleVocabulary(
            [SimpleTerm(title=_(u"Sí"), value=True),
             SimpleTerm(title=_(u"No"), value=False),
             SimpleTerm(title=_(u"Desconeguda"), value=None)]),
        required=False,
    )

    quota_import = schema.Float(
        title=_(u"Import"),
        required=False)

    quota_moneda = schema.TextLine(
        title=_(u"Moneda"),
        required=False)

    quota_observacions = schema.Text(
        title=_(u"Observacions"),
        required=False)

    directives.mode(unitat_carrec='hidden')
    textindexer.searchable('unitat_carrec')
    unitat_carrec = schema.TextLine(
        title=_(u"Unitat de càrrec"),
        required=False)

    percentatge_participacio = schema.Float(
        title=_(u"% UPC en capital"),
        required=False)

    directives.mode(title2='display')
    title2 = schema.TextLine(
        title=_(u""),
        default=_(u"2. A òrgan de govern superior"),
    )

    total_membres = schema.Int(
        title=_(u"Membres totals"),
        required=False)

    textindexer.searchable('nombre_membres')
    nombre_membres = schema.TextLine(
        title=_(u"Membres UPC als òrgans de govern"),
        required=False)

    percentatge_membres = schema.Float(
        title=_(u"% UPC en vots"),
        required=False)

    membres_observacions = schema.Text(
        title=_(u"Observacions"),
        required=False)

    directives.widget(capital_social_sn=RadioFieldWidget)
    directives.omitted('capital_social_sn')
    capital_social_sn = schema.Choice(
        title=_(u"Participació en capital social o fons patrimonial"),
        vocabulary=SimpleVocabulary(
            [SimpleTerm(title=_(u"Sí"), value=True),
             SimpleTerm(title=_(u"No"), value=False),
             SimpleTerm(title=_(u"Desconeguda"), value=None)]),
        required=False,
    )

    capital_social_import = schema.Float(
        title=_(u"Fons patrimonial"),
        required=False)

    capital_social_moneda = schema.TextLine(
        title=_(u"Moneda"),
        required=False)

    textindexer.searchable('participacio_observacions')
    participacio_observacions = schema.Text(
        title=_(u"Observacions"),
        required=False)

    model.fieldset(
        "marc_legal",
        label=u"Marc legal",
        fields=['entitats_constituents', 'entitats_actuals',
                'data_constitucio', 'data_entrada',
                'data_baixa', 'data_entrada_acord', 'data_baixa_acord',
                'data_entrada_procediment', 'data_baixa_procediment',
                'seu_social', 'seu_social_estranger', 'adscripcio',
                'marc_legal_observacions'])

    textindexer.searchable('entitats_constituents')
    entitats_constituents = schema.Text(
        title=_(u"Entitats constituents"),
        required=False)

    textindexer.searchable('entitats_actuals')
    entitats_actuals = schema.Text(
        title=_(u"Entitats actuals"),
        required=False)

    data_constitucio = schema.Date(
        title=_(u"Data de constitució"),
        required=False)

    data_entrada = schema.Date(
        title=_(u"Data d'alta UPC"),
        required=False)

    textindexer.searchable('data_entrada_acord')
    data_entrada_acord = schema.TextLine(
        title=_(u"Acord d'alta"),
        required=False)

    textindexer.searchable('data_entrada_procediment')
    data_entrada_procediment = schema.Text(
        title=_(u"Procediment d'alta"),
        required=False)

    data_baixa = schema.Date(
        title=_(u"Data de baixa UPC"),
        required=False,)

    textindexer.searchable('data_baixa_acord')
    data_baixa_acord = schema.TextLine(
        title=_(u"Acord de baixa"),
        required=False)

    textindexer.searchable('data_baixa_procediment')
    data_baixa_procediment = schema.Text(
        title=_(u"Procediment de baixa"),
        required=False)

    seu_social = schema.Choice(
        title=_(u"Àmbit legislatiu"),
        vocabulary=get_vocabulary([
            u"-",
            u"Catalunya",
            u"Resta d'Espanya",
            u"Estranger"]),
        default="-",
        required=False)

    seu_social_estranger = schema.TextLine(
        title=_(u"Seu social a l'estranger"),
        required=False)

    textindexer.searchable('adscripcio')
    adscripcio = schema.TextLine(
        title=_(u"Adm. Pública d'adscripció"),
        required=False)

    textindexer.searchable('marc_legal_observacions')
    marc_legal_observacions = schema.Text(
        title=_(u"Observacions"),
        required=False)


@implementer(IEns)
class Ens(Item):
    pass


def get_denominacio(ens):
        if ens.acronim:
            return "{0} ({1})".format(
                ens.title.encode("utf-8"),
                ens.acronim.encode("utf-8")).decode("utf-8")
        else:
            return ens.title


def get_percentatge_participacio(ens):
        if ens.percentatge_participacio:
            return "{0:,.2f}%".format(ens.percentatge_participacio)
        else:
            return "-"


def get_percentatge_membres(ens):
        if ens.percentatge_membres:
            return "{0:,.2f}%".format(ens.percentatge_membres)
        else:
            return "-"


def get_observacions(ens, section):
    obs = getattr(ens, section + '_observacions')
    if obs:
        return obs
    else:
        return False


def get_data_participacio(ens):
    return ens.participacio_data.strftime('%d/%m/%Y') if ens.participacio_data else "-"


def get_aportacio_total(ens):
    if ens.aportacio_total:
        moneda = "" if ens.aportacio_total_moneda is None \
                 else " " + ens.aportacio_total_moneda.encode("utf-8")
        return "{0:,.2f}{1}".format(
            ens.aportacio_total, moneda).decode('utf-8')
    else:
        return '-'


def get_aportacio(ens):
    if ens.aportacio_import:
        moneda = "" if ens.aportacio_moneda is None \
                 else " " + ens.aportacio_moneda.encode("utf-8")
        return "{0:,.2f}{1}".format(
            ens.aportacio_import, moneda).decode('utf-8')
    else:
        return '-'


def get_quota(ens):
    if ens.quota_import:
        moneda = "" if ens.quota_moneda is None \
            else " " + ens.quota_moneda.encode("utf-8")
        return "{0:,.2f}{1}".format(
            ens.quota_import, moneda).decode('utf-8')
    else:
        return '-'


def get_capital_social(ens):
    if ens.capital_social_import:
        moneda = "" if ens.capital_social_moneda is None \
            else " " + ens.capital_social_moneda.encode("utf-8")
        return "{0:,.2f}{1}".format(
            ens.capital_social_import, moneda).decode('utf-8')
    else:
        return '-'


def get_capital_social_data(ens):
    capital_social = get_capital_social(ens)
    data_participacio = get_data_participacio(ens)
    if capital_social == '-' and data_participacio == '-':
        return '-'
    return capital_social + " (" + data_participacio + ")"


def get_seu_social(ens):
    if ens.seu_social:
        if ens.seu_social == u"Estranger":
            if ens.seu_social_estranger:
                return ens.seu_social_estranger
            else:
                return ens.seu_social
        else:
            return ens.seu_social
    else:
        return "-"


@implementer(IEns)
class Ens(Container):

    @property
    def b_icon_expr(self):
        return "building"


class View(BrowserView):

    @property
    def percentatge_participacio(self):
        return get_percentatge_participacio(self.context)

    @property
    def percentatge_membres(self):
        return get_percentatge_membres(self.context)

    @property
    def observacions_participacio(self):
        return get_observacions(self.context, 'participacio')

    @property
    def observacions_membres(self):
        return get_observacions(self.context, 'membres')

    @property
    def observacions_quota(self):
        return get_observacions(self.context, 'quota')

    @property
    def data_participacio(self):
        return get_data_participacio(self.context)

    @property
    def aportacio_total(self):
        return get_aportacio_total(self.context)

    @property
    def aportacio(self):
        return get_aportacio(self.context)

    @property
    def quota(self):
        return get_quota(self.context)

    @property
    def capital_social(self):
        return get_capital_social(self.context)

    @property
    def seu_social(self):
        return get_seu_social(self.context)

    @property
    def adscripcio(self):
        return self.context.adscripcio or "-"

    @property
    def unitats(self):
        reporter = EnsDataReporter(api.portal.get_tool("portal_catalog"))
        return reporter.list_unitats_by_ens_obj(self.context)

    @property
    def acords(self):
        reporter = EnsDataReporter(api.portal.get_tool("portal_catalog"))
        return reporter.list_acords_by_ens_obj(self.context)

    @property
    def estatuts_vigents(self):
        reporter = EnsDataReporter(api.portal.get_tool("portal_catalog"))
        return reporter.list_estatuts_by_ens_obj(self.context, is_vigent=True)

    @property
    def estatuts_historics(self):
        reporter = EnsDataReporter(api.portal.get_tool("portal_catalog"))
        return reporter.list_estatuts_by_ens_obj(self.context, is_vigent=False)

    @property
    def escriptures(self):
        reporter = EnsDataReporter(api.portal.get_tool("portal_catalog"))
        return reporter.list_escriptures_by_ens_obj(self.context)

    @property
    def documents_interes(self):
        reporter = EnsDataReporter(api.portal.get_tool("portal_catalog"))
        return reporter.list_documents_interes_by_ens_obj(self.context)

    @property
    def convenis(self):
        reporter = EnsDataReporter(api.portal.get_tool("portal_catalog"))
        return reporter.list_convenis_by_ens_obj(self.context)

    @property
    def actes_reunio(self):
        reporter = EnsDataReporter(api.portal.get_tool("portal_catalog"))
        return reporter.list_actes_reunio_by_ens_obj(self.context)

    @property
    def organs_govern(self):
        reporter = EnsDataReporter(api.portal.get_tool("portal_catalog"))
        return reporter.list_organs_by_ens(self.context, tipus="Govern")

    @property
    def organs_assessors(self):
        reporter = EnsDataReporter(api.portal.get_tool("portal_catalog"))
        return reporter.list_organs_by_ens(self.context, tipus="Assessor")

    @property
    def directius(self):
        reporter = EnsDataReporter(api.portal.get_tool("portal_catalog"))
        return reporter.list_directius_by_ens_obj(self.context)

    @property
    def contactes(self):
        reporter = EnsDataReporter(api.portal.get_tool("portal_catalog"))
        return reporter.list_contactes_by_ens_obj(self.context)

    def get_file_href(self, content):
        return "{0}/view/++widget++form.widgets.fitxer/@@download/{1}".format(
            content.absolute_url(), content.fitxer.filename.encode('utf-8'))

    def list_carrecs_by_organ(self, organ, is_historic=None):
        reporter = EnsDataReporter(api.portal.get_tool("portal_catalog"))
        return reporter.list_carrecs_by_organ_grouped_by_ens_obj(
            organ, is_historic=is_historic)

    def prettify_organ_title(self, organ):
        return "{0}{1}".format(
            organ.Title,
            _(u" (Històric)").encode('utf-8') if organ.is_historic else u"")

    def getData(self):
        ens = self.context
        if ens.estat == 'Actiu':
            data = ens.data_entrada.strftime('%d/%m/%Y') if ens.data_entrada else '-'
        elif ens.estat == 'Baixa':
            data = ens.data_baixa.strftime('%d/%m/%Y') if ens.data_baixa else '-'
        else:
            data = '-'
        return data