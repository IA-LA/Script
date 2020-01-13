""""
Created on 02-12-2019

@author: FJSB

"""

import sys

from doi.ProcesoParametros import *
from doi.ProcesoFichero import *
from doi.ProcesoXhtml import *
# from doi.ProcesoUrl import *

if __name__ == '__main__':

    ###########
    # PRUEBAS #
    ###########

    # FILTRA LOS PARAMETROS (de línea de comandos)
    ficheros = filtrar_parametros(sys.argv)
    print(ficheros)
    #exit(999)

    # PARA CADA FICHERO #
    for index, fichero in enumerate(ficheros):

        # INICIALIZAR lista
        lista = []
        
        # print(fichero)
        
        # Maneja Dict as Object
        class AttributeDict(dict):
            def __getattr__(self, name):
                if name in self:
                    return self[name]
                raise AttributeError(name)


        fichero = AttributeDict(fichero)

        # Obtiene la lista de LINK y DOI
        lista = ['https://dx.doi.org/10.1037/14342-008.', 'https://dx.doi.org/10.1080/08995600701323277.',
                 'https://dx.doi.org/10.1089/15246090152563515.', 'https://dx.doi.org/10.1037/0033-2909.117.3.497.',
                 'https://dx.doi.org/10.1037/0021-9010.88.6.989.', 'https://dx.doi.org/10.1080/00224545.2015.1071767.',
                 'https://dx.doi.org/10.1080/00223980903218273.', 'https://dx.doi.org/10.1037/0022-3514.34.3.366.',
                 'https://dx.doi.org/10.1002/j.2051-5545.2009.tb00218.x/full',
                 'https://dx.doi.org/10.1177/0146167295216003.', 'https://dx.doi.org/10.1037/1089-2699.4.1.7.',
                 'https://dx.doi.org/10.1037/0003-066X.39.8.885.', 'https://dx.doi.org/10.1016/j.rpto.2016.06.002.',
                 'https://dx.doi.org/10.1146/annurev.psych53.100901.135109',
                 'https://dx.doi.org/10.1037/0022-006X.46.6.117.',
                 'https://dx.doi.org/10.1111/j.1559-1816.1988.tb00032', 'https://dx.doi.org/10.1111/1540-4560',
                 'https://dx.doi.org/10.1207/s15327876mp1101_4.', 'https://dx.doi.org/10.6018/analesps.29-.2.139241',
                 'https://dx.doi.org/10.6224/JN.59.3.62', 'https://dx.doi.org/10.1037//O022-3514.79.5.748']

        print('*********************')
        print('LISTA URL FICHERO:', fichero.nombreyextension)
        print('*********************')

        lista = generar_lista(fichero.rutaynombreyextension)
        
        print('LISTA DE URL FALLIDAS', lista)
        
        generar_txt(fichero.rutaynombreyextension, lista)
