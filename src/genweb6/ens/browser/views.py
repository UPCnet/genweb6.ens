# -*- coding: utf-8 -*-

from Products.Five.browser import BrowserView
from io import StringIO

from plone import api

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
        output_file.write(u'\ufeff'.encode('utf8'))
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
                representant.title.encode('utf-8'),
                representant.dni.encode('utf-8'),
                representant.carrec.encode('utf-8')
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
