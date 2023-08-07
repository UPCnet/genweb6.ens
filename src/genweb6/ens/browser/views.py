# -*- coding: utf-8 -*-

from Products.Five.browser import BrowserView
from Products.PythonScripts.standard import url_quote

from io import StringIO
from plone import api

from genweb6.ens import _
from genweb6.ens import utils
from genweb6.ens.content.ens import ens
from genweb6.ens.data_access.carrec import CarrecDataReporter
from genweb6.ens.data_access.ens import EnsDataReporter

import csv
import json
import transaction


def getRepresentantsUPC():
    catalog = api.portal.get_tool('portal_catalog')
    root_path = '/'.join(api.portal.get().getPhysicalPath())
    language = api.portal.get_current_language()
    path = root_path + '/' + language + '/administrar-persones/persones'
    return catalog(portal_type=('genweb.ens.representant'),
                   path=path)


class TaulaRepresentatsUpc(BrowserView):

    def list(self):
        return getRepresentantsUPC()

    @property
    def export_url(self):
        return '{0}/taula_representants_upc_csv'.format(self.context.absolute_url())


class TaulaRepresentatsUpcCsv(BrowserView):

    data_header_columns = [
        "Representant",
        "DNI",
        "Col·lectiu"]

    def __call__(self):
        output_file = StringIO()
        # Write the BOM of the text stream to make its charset explicit
        output_file.write(u'\ufeff')
        self.write_data(output_file)

        header_content_type = 'text/csv'
        header_filename = 'taula_representants_upc.csv'
        self.request.response.setHeader('Content-Type', header_content_type)
        self.request.response.setHeader(
            'Content-Disposition',
            'attachment; filename="{0}"'.format(header_filename))
        return output_file.getvalue()

    def list(self):
        return getRepresentantsUPC()

    def write_data(self, output_file):
        writer = csv.writer(output_file, dialect='excel', delimiter=';')
        writer.writerow(TaulaRepresentatsUpcCsv.data_header_columns)

        for representant in self.list():
            representant = representant.getObject()

            if representant.dni is None:
                representant.dni = ''
            if representant.carrec is None:
                representant.carrec = ''

            writer.writerow([
                representant.title,
                representant.dni,
                representant.carrec
            ])


class Taula(BrowserView):

    def parse_search_filters(self):
        search_filters = {}
        try:
            carpetes = json.loads(self.request.form.get('carpetes', ''))
            if carpetes:
                search_filters["path"] = {"depth": 1}
                search_filters["path"]["query"] = [
                    carpeta for carpeta in carpetes]
        except ValueError:
            pass
        return search_filters


class TauladEntitats(Taula):

    def list(self):
        reporter = EnsDataReporter(api.portal.get_tool('portal_catalog'))
        return reporter.list_entitats(self.parse_search_filters())

    @property
    def export_url(self):
        query_string = 'carpetes=' + self.request.form.get('carpetes', '')
        return '{0}/taula_dentitats_csv?{1}'.format(
            self.context.absolute_url(), query_string)

    def getSeu(self, ens):
        if 'Estranger' in ens.seu_social:
            seu = ens.seu_social + ' (' + ens.seu_social_estranger + ')'
        else:
            seu = ens.seu_social
        return seu

    def getTags(self, ens):
        tags = []
        lang = api.portal.get_current_language()
        portal_url = api.portal.get().absolute_url() + '/' + lang
        categories = ens.tags
        try:
            for category in categories():
                quotedCat = url_quote(category)
                tag_link = portal_url + '/@@search?Subject%3Alist=' + quotedCat
                tag = {'tag_name': category, 'tag_url': tag_link}
                tags.append(tag)
            return tags
        except:
            return []


class TauladEntitatsCsv(Taula):

    data_header_columns = [
        "Denominació",
        "Acrònim",
        "Estat",
        "NIF",
        "Àmbit institucional",
        "Figura jurídica",
        "Identificadors",
        "Web",
        "Tipologia UPC",
        "Codi UPC",
        "Núm. UPC",
        "Etiquetes",
        "Data alta UPC",
        "Data baixa UPC",
        "Fons patrimonial (data)",
        "Cap. inicial total",
        "Aportació inicial UPC",
        "% UPC en capital",
        "% UPC en vots",
        "Quota",
        "Entitats constituents",
        "Entitats actuals",
        "Data de constitució",
        "Data alta UPC",
        "Acord UPC",
        "Adscripció",
        "Data estatuts"]

    def __call__(self):
        output_file = StringIO()
        # Write the BOM of the text stream to make its charset explicit
        output_file.write(u'\ufeff')
        self.write_data(output_file)

        header_content_type = 'text/csv'
        header_filename = 'taula_d\'entitats.csv'
        self.request.response.setHeader('Content-Type', header_content_type)
        self.request.response.setHeader(
            'Content-Disposition',
            'attachment; filename="{0}"'.format(header_filename))
        return output_file.getvalue()

    def write_data(self, output_file):
        reporter = EnsDataReporter(api.portal.get_tool('portal_catalog'))
        writer = csv.writer(output_file, dialect='excel', delimiter=';')
        writer.writerow(TauladEntitatsCsv.data_header_columns)

        for ens in reporter.list_entitats(self.parse_search_filters()):
            ens_tags = ",".join([str(tag) for tag in ens.tags()])
            if ens.entitats_constituents and ens.entitats_constituents != '-':
                pass

            writer.writerow([
                ens.title or "-",
                ens.acronim or "-",
                ens.estat or "-",
                ens.nif or "-",
                ens.institution_type or "-",
                ens.figura_juridica or "-",
                ens.numero_identificacio or "-",
                ens.web or "-",
                ens.tipologia_upc or "-",
                ens.codi or "-",
                ens.num_ens or "-",
                ens_tags or "-",
                ens.data_entrada or "-",
                ens.data_baixa or "-",
                ens.capital_social or "-",
                ens.aportacio_total or "-",
                ens.aportacio_import or "-",
                ens.percentatge_participacio or "-",
                ens.percentatge_membres or "-",
                ens.quota or "-",
                ens.entitats_constituents or "-",
                ens.entitats_actuals or "-",
                ens.data_constitucio or "-",
                ens.data_entrada or "-",
                ens.data_entrada_acord or "-",
                ens.adscripcio or "-",
                ens.data_estatuts or "-"
            ])


class TaulaRepresentacio(Taula):

    def list(self):
        reporter = EnsDataReporter(api.portal.get_tool('portal_catalog'))
        return reporter.list_representacio(
            is_historic=False,
            search_filters=self.parse_search_filters())

    @property
    def export_url(self):
        query_string = 'carpetes=' + self.request.form.get('carpetes', '')
        return '{0}/taula_representacio_csv?{1}'.format(
            self.context.absolute_url(), query_string)


class TaulaRepresentacioCsv(Taula):

    data_header_columns = [
        "Denominació",
        "Acrònim",
        "Òrgan",
        "Càrrec a l'òrgan",
        "Nom persona",
        "En qualitat de ...",
        "Data inici",
        "Vigència",
        "Data fi"]

    def __call__(self):
        output_file = StringIO()
        # Write the BOM of the text stream to make its charset explicit
        output_file.write(u'\ufeff')
        self.write_data(output_file)

        header_content_type = 'text/csv'
        header_filename = 'taula_representacio.csv'
        self.request.response.setHeader('Content-Type', header_content_type)
        self.request.response.setHeader(
            'Content-Disposition',
            'attachment; filename="{0}"'.format(header_filename))
        return output_file.getvalue()

    def write_data(self, output_file):
        reporter = EnsDataReporter(api.portal.get_tool('portal_catalog'))
        writer = csv.writer(output_file, dialect='excel', delimiter=';')
        writer.writerow(TaulaRepresentacioCsv.data_header_columns)

        for ens in reporter.list_representacio(
                is_historic=False,
                search_filters=self.parse_search_filters()):
            writer.writerow([
                ens.denominacio or "-",
                ens.acronim or "-",
                ens.organ or "-",
                ens.carrec or "-",
                ens.persona or "-",
                ens.qualitat or "-",
                ens.data_inici or "-",
                ens.vigencia or "-",
                ens.data_fi or "-",
            ])


class FixCarrecRepresents(BrowserView):

    def __call__(self):
        representants = getRepresentantsUPC()
        for representant in representants:
            obj = representant.getObject()
            if obj.carrec == 'Externs CS':
                obj.carrec = 'Extern CS'
                obj.reindexObject()

        transaction.commit()
        return 'Done!'

class EnsSearch(BrowserView):

    @property
    def figura_juridica_vocabulary(self):
        return [('', _(u"Qualsevol"))] + [
            (value, value) for value in ens.figura_juridica_values]

    @property
    def estat_vocabulary(self):
        return [('', _(u"Qualsevol"))] + [
            (value, value) for value in ens.estat_values]

    @property
    def carpetes_vocabulary(self):
        return utils.get_carpetes_vocabulary(self)


class EnsSearchResults(BrowserView):

    def parse_search_filters(self):
        search_filters = {}

        figura_juridica = self.request.form.get('figura_juridica', '')
        if figura_juridica:
            search_filters['figura_juridica'] = figura_juridica

        estat = self.request.form.get('estat', '')
        if estat:
            search_filters['estat'] = estat

        try:
            carpetes = json.loads(self.request.form.get('carpetes', ''))
            if carpetes:
                search_filters["path"] = {"depth": 1}
                search_filters["path"]["query"] = carpetes
        except ValueError:
            pass

        text = self.request.form.get('text', None)
        if text:
            search_filters['SearchableText'] = "*{0}*".format(text)

        return search_filters

    def search(self):
        reporter = EnsDataReporter(api.portal.get_tool('portal_catalog'))
        return reporter.search(self.parse_search_filters())


class CarrecSearch(BrowserView):

    @property
    def carpetes_vocabulary(self):
        return utils.get_carpetes_vocabulary(self)


class CarrecSearchResults(BrowserView):

    def parse_search_filters(self):
        search_filters = {}

        text = self.request.form.get('text', None)
        if text:
            search_filters['Title'] = "*{0}*".format(text)

        try:
            carpetes = json.loads(self.request.form.get('carpetes', ''))
            if carpetes:
                search_filters["path"] = {"depth": 3}
                search_filters["path"]["query"] = carpetes
        except ValueError:
            pass

        historics = self.request.form.get('historics', False)
        if not historics or historics == 'false':
            search_filters['is_historic'] = False

        return search_filters

    def search(self):
        reporter = CarrecDataReporter(api.portal.get_tool('portal_catalog'))
        return reporter.search(self.parse_search_filters())
