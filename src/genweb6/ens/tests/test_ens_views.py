# -*- coding: utf-8 -*-

"""Functional tests for ens views."""

from plone.testing.z2 import Browser
from transaction import commit

from genweb6.ens.testing import FunctionalTestCase
from genweb6.ens.tests.fixtures import fixtures


class TestEnsViews(FunctionalTestCase):
    """Test taula views functions."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.browser = Browser(self.layer['portal'])

    def assertAppearsBefore(self, subtxt_1, subtxt_2, txt):
        self.assertIn(subtxt_1, txt)
        self.assertIn(subtxt_2, txt)
        self.assertTrue(txt.find(subtxt_1) < txt.find(subtxt_2))

    def assertAppearInOrder(self, subtxts, txt):
        def assertAppearsBefore(subtxt_1, subtxt_2):
            self.assertAppearsBefore(subtxt_1, subtxt_2, txt)
            return subtxt_2
        reduce(assertAppearsBefore, subtxts)

    def test_view_displays_all_fields_in_order(self):
        ens = fixtures.create_content(self.layer['portal'], fixtures.ens_ai)
        directiu_1 = fixtures.create_content(ens, fixtures.persona_directiu_1)
        directiu_2 = fixtures.create_content(ens, fixtures.persona_directiu_2)
        contacte_1 = fixtures.create_content(ens, fixtures.persona_contacte_1)
        contacte_2 = fixtures.create_content(ens, fixtures.persona_contacte_2)
        organ_2 = fixtures.create_content(ens, fixtures.organ_2)
        organ_3 = fixtures.create_content(ens, fixtures.organ_3)
        organ_1 = fixtures.create_content(ens, fixtures.organ_1)
        organ_5 = fixtures.create_content(ens, fixtures.organ_5)
        organ_4 = fixtures.create_content(ens, fixtures.organ_4)
        organ_6 = fixtures.create_content(ens, fixtures.organ_6)
        carrec_1 = fixtures.create_content(organ_1, fixtures.carrec_1)
        carrec_2 = fixtures.create_content(organ_1, fixtures.carrec_2)
        carrec_3 = fixtures.create_content(organ_1, fixtures.carrec_3)
        carrec_4 = fixtures.create_content(organ_1, fixtures.carrec_4)
        carrec_5 = fixtures.create_content(organ_1, fixtures.carrec_5)
        unitat_1 = fixtures.create_content(ens, fixtures.unitat_1)
        unitat_2 = fixtures.create_content(ens, fixtures.unitat_2)
        acord_1 = fixtures.create_content(ens, fixtures.acord_1)
        acord_2 = fixtures.create_content(ens, fixtures.acord_2)
        acord_3 = fixtures.create_content(ens, fixtures.acord_3)
        acord_4 = fixtures.create_content(ens, fixtures.acord_4)
        escriptura_1 = fixtures.create_content(ens, fixtures.escriptura_1)
        escriptura_2 = fixtures.create_content(ens, fixtures.escriptura_2)
        escriptura_3 = fixtures.create_content(ens, fixtures.escriptura_3)
        escriptura_4 = fixtures.create_content(ens, fixtures.escriptura_4)
        estatut_1 = fixtures.create_content(ens, fixtures.estatut_1)
        estatut_2 = fixtures.create_content(ens, fixtures.estatut_2)
        estatut_3 = fixtures.create_content(ens, fixtures.estatut_3)
        estatut_4 = fixtures.create_content(ens, fixtures.estatut_4)
        estatut_5 = fixtures.create_content(ens, fixtures.estatut_5)
        estatut_6 = fixtures.create_content(ens, fixtures.estatut_6)
        conveni_1 = fixtures.create_content(ens, fixtures.conveni_1)
        conveni_2 = fixtures.create_content(ens, fixtures.conveni_2)
        conveni_3 = fixtures.create_content(ens, fixtures.conveni_3)
        commit()

        self.browser.open(ens.absolute_url())

        self.assertAppearInOrder([
            "<dt>Denominació</dt>",
            "<dd>{0}</dd>".format(ens.title),
            "<dt>Acrònim</dt>",
            "<dd>{0}</dd>".format(ens.acronim),
            "<dt>Objecte social</dt>",
            '<dd class="fieldset-end">{0}</dd>'.format(
                ens.objecte_social),
            "<dt>Estat</dt>",
            "<dd>{0}</dd>".format(ens.estat),
            "<dt>NIF</dt>",
            "<dd>{0}</dd>".format(ens.nif),
            '<dt>Figura jurídica</dt>',
            "<dd>{0}</dd>".format(
                ens.figura_juridica),
            '<dt class="subfield">Núm. Identif.</dt>',
            '<dd class="fieldset-end">{0}</dd>'.format(
                ens.numero_identificacio),
            "<dt>Domicili social (població)</dt>",
            "<dd>{0}</dd>".format(
                ens.domicili_social_poblacio),
            "<dt>Domicili social (adreça)</dt>",
            "<dd>{0}</dd>".format(ens.domicili_social_adreca),
            "<dt>Adreça 2</dt>",
            "<dd>{0}</dd>".format(ens.adreca_2),
            "<dt>Telèfon</dt>",
            "<dd>{0}</dd>".format(ens.telefon),
            "<dt>Fax</dt>",
            "<dd>{0}</dd>".format(ens.fax),
            "<dt>Web</dt>",
            '<dd class="fieldset-end">{0}</dd>'.format(
                ens.web),
            "<dt>Tipologia UPC</dt>",
            "<dd>{0}</dd>".format(ens.tipologia_upc),
            "<dt>Codi UPC</dt>",
            '<dd>{0}</dd>'.format(ens.codi),
            "<dt>Etiquetes</dt>",
            '<dd class="fieldset-end">{0}</dd>'.format(
                ens.etiquetes),
            ], self.browser.contents)

        self.assertIn("<h3>Càrrecs directius</h3>", self.browser.contents)

        for directiu in (directiu_1, directiu_2):
            self.assertIn(directiu.title,
                          self.browser.contents)
            self.assertIn(directiu.carrec,
                          self.browser.contents)
            self.assertIn(directiu.telefon,
                          self.browser.contents)
            self.assertIn(directiu.email,
                          self.browser.contents)

        self.assertIn("<h3>Persones de contacte</h3>", self.browser.contents)

        for contacte in (contacte_1, contacte_2):
            self.assertIn(contacte.title,
                          self.browser.contents)
            self.assertIn(contacte.carrec,
                          self.browser.contents)
            self.assertIn(contacte.telefon,
                          self.browser.contents)
            self.assertIn(contacte.email,
                          self.browser.contents)

        self.assertIn("<dt>Aportació inicial</dt>", self.browser.contents)
        self.assertIn("<dd>2,300.50 €/any</dd>", self.browser.contents)

        self.assertIn("<dt>Quota</dt>", self.browser.contents)
        self.assertIn("<dd>253.44 €/mes</dd>", self.browser.contents)

        self.assertIn("<dt>Unitat de càrrec</dt>", self.browser.contents)
        self.assertIn("<dd>{0}</dd>".format(ens.unitat_carrec),
                      self.browser.contents)

        self.assertIn("<dt>Percentatge de participació</dt>",
                      self.browser.contents)
        self.assertIn("<dd>15.35%</dd>", self.browser.contents)

        self.assertIn("<dt>Membres UPC als òrgans de govern</dt>",
                      self.browser.contents)
        self.assertIn("<dd>{0}</dd>".format(
            ens.nombre_membres),
            self.browser.contents)

        self.assertIn("<dt>Part. en cap. social o fons patrimonial</dt>",
                      self.browser.contents)
        self.assertIn("<dd>2,000.00 EUR</dd>", self.browser.contents)

        self.assertAppearInOrder([
            organ_2.title + u" (Històric)",
            organ_3.title,
            organ_1.title,
            organ_5.title,
            organ_4.title,
            organ_6.title],
            self.browser.contents)

        self.assertAppearsBefore(
            "<h3>Òrgans de govern</h3>",
            organ_1.title,
            self.browser.contents)

        self.assertAppearInOrder([
            carrec_1.title,
            carrec_2.title,
            carrec_4.title,
            carrec_3.title,
            carrec_5.title],
            self.browser.contents)

        self.assertAppearsBefore(
            "<h3>Òrgans assessors</h3>",
            organ_4.title,
            self.browser.contents)

        self.assertAppearInOrder([
            "<h3>Unitats UPC implicades</h3>",
            unitat_2.title,
            unitat_1.title],
            self.browser.contents)

        self.assertIn("<dt>Data de constitució</dt>", self.browser.contents)
        self.assertIn("<dd>17/02/2005</dd>", self.browser.contents)

        self.assertIn("<dt>Entitats constituents</dt>", self.browser.contents)
        self.assertIn("<dd>{0}</dd>".format(
            ens.entitats_constituents), self.browser.contents)

        self.assertIn("<dt>Entitats actuals</dt>", self.browser.contents)
        self.assertIn("<dd>{0}</dd>".format(
            ens.entitats_actuals), self.browser.contents)

        self.assertIn("<dt>Data d&apos;entrada UPC</dt>",
                      self.browser.contents)
        self.assertIn("<dd>11/03/2015</dd>", self.browser.contents)

        self.assertIn('<dt class="subfield">Procediment d&apos;entrada</dt>',
                      self.browser.contents)
        self.assertIn("<dd>{0}</dd>".format(
            ens.data_entrada_procediment),
            self.browser.contents)

        self.assertIn("<dt>Seu social</dt>", self.browser.contents)
        self.assertIn("<dd>{0}</dd>".format(
            ens.seu_social), self.browser.contents)

        self.assertIn("<dt>Adm. Pública d&apos;adscripció</dt>",
                      self.browser.contents)
        self.assertIn("<dd>{0}</dd>".format(
            ens.adscripcio), self.browser.contents)

        self.assertAppearInOrder([
            "<h3>Acords UPC</h3>",
            acord_1.title,
            acord_4.title,
            acord_2.title,
            acord_3.title],
            self.browser.contents)

        self.assertAppearInOrder([
            "<h3>Documents públics</h3>",
            escriptura_4.title,
            escriptura_1.title,
            escriptura_2.title,
            escriptura_3.title],
            self.browser.contents)

        self.assertAppearInOrder([
            "<h3>Estatuts i normatives</h3>",
            "<h4>Vigents</h4>",
            estatut_2.title,
            estatut_3.title,
            estatut_1.title,
            "<h4>Anteriors</h4>",
            estatut_4.title,
            estatut_6.title,
            estatut_5.title],
            self.browser.contents)

        self.assertAppearInOrder([
            "<h3>Convenis</h3>",
            conveni_3.title,
            conveni_1.title,
            conveni_2.title],
            self.browser.contents)

        self.assertIn(
            "<h3>Altres documents d&apos;interès</h3>",
            self.browser.contents)
