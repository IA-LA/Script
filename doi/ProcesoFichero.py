""""
Created on 04-12-2019

@author: FJSB

Genera el archivo de salida

"""

import io
import os
#from types import *

import csv


def generar_txt(path, contenido=''):

    print('Generando Fichero TXT', path, os.path.splitext(path)[0] + '_erores.txt')

    # Fichero destino
    ruta_txt = os.path.splitext(path)[0] + '_erores.txt'
    
    #print(type(contenido), isinstance(contenido, list))
    
    # CONTENIDO tipo STRING
    if contenido == '':
        # Copia origen
        with io.open(path, 'r', encoding='iso-8859-1') as f:
            text = f.read()
        # Pega detino
        with io.open(ruta_txt, 'w', encoding='utf8') as f:
            f.write(text)
    # CONTENIDO tipo LISTA
    elif isinstance(contenido, list):
        i = 0
        # Pega contenido
        for elemento in contenido:
            if i == 0:
                with io.open(ruta_txt, 'w', encoding='utf8') as f:
                    f.write(str(elemento) + '\n')
                i = 1
            else:
                with io.open(ruta_txt, 'a', encoding='utf8') as f:
                    f.write(str(elemento) + '\n')
        # Fichero vacío si lista vacía
        # if i == 0:
        #        with io.open(ruta_txt, 'w', encoding='utf8') as f:
        #            f.write('\n')
    # CONTENIDO tipo TIPO
    else:
        with io.open(ruta_txt, 'w', encoding='utf8') as f:
            f.write(contenido)
    
    return ruta_txt


def generar_csv(nombre_txt, lista_mensajes):

    ruta_csv = nombre_txt + '.csv'
    keys = lista_mensajes[0].keys()

    print('Generando 3', nombre_txt, lista_mensajes[0], ruta_csv)

    with open(ruta_csv, 'w', encoding='utf8') as output_file:  # Just use 'w' mode in 3.x
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(lista_mensajes)

    print('Generando 3', ruta_csv, keys)

    print('Fichero CSV general creado: ' + ruta_csv)

    return ruta_csv
