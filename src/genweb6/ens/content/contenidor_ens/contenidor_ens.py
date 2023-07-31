# -*- coding: utf-8 -*-

from zope.interface import implementer
from plone.dexterity.content import Container

from genweb6.ens.content.contenidor.contenidor import IContenidor


class IContenidorEns(IContenidor):
    pass


@implementer(IContenidorEns)
class ContenidorEns(Container):

    @property
    def b_icon_expr(self):
        return "folder"