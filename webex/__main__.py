""""
Created on 09-01-2020

@author: FJSB

"""

import sys

from webex.ProcesoParametros import *
from webex.ProcesoFichero import *
from webex.ProcesoXhtml import *
from webex.ProcesoUrl import *

if __name__ == '__main__':

    ###########
    # PRUEBAS #
    ###########
    #get_url("http://example.com/foo/bar")
    #get_url("https://idpf.github.io/epub-vocabs/package/item/#sec-item-property-values")
    # CURSOS
    get_url_curso("http://extension.uned.es/actividad/idactividad/19934")
    # LISTA DE BUSQUEDA
    #get_url_actividades("http://extension.uned.es")
    #get_url_actividades("http://extension.uned.es/indice&tiempo=2019")
    get_url_actividades("http://extension.uned.es/indice&tiempo=2020")
