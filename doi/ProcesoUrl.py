""""
Created on 03-12-2019

@author: FJSB

Opciones de verificación de URL

"""

import http.client
import urllib.parse
import urllib.request
from bs4 import BeautifulSoup


# funcion que se encarga de obtener respuesta del estatus del servidor web
# HTTP.CLIENT
def get_server_status_code(url):
    print(url)
    # descarga sólo el encabezado de una URL y devolver el código de estado del servidor.
    host, path = urllib.parse.urlparse(url)[1:3]
    try:
        conexion = http.client.HTTPConnection(host)
        conexion.request('HEAD', path)
        # print(conexion.getresponse().status)
        
        return conexion.getresponse().status
    except Exception as e:
        return e


# funcion que se encarga de obtener respuesta del estatus del servidor web
# URLLIB.PARSE
def get_server_status_code1(url):
    try:
        parsed_url = urllib.parse.urlparse(url)
        # print(bool(parsed_url.scheme))
        
        return bool(parsed_url.scheme)
    except Exception as e:
        return e


# funcion que se encarga de obtener respuesta del estatus del servidor web
# URLLIB.REQUEST
def get_server_status_code2(url):
    try:
        page = urllib.request.urlopen(url)
        soup = BeautifulSoup(page, "html5lib")
        # print(soup.title.string)
        
        return soup.title.string
    except Exception as e:
        return e


# función que se encarga de checkear que exista la url a guardar
def check_url(url):

    # 1
    codigo = get_server_status_code(url)

    # 2
    codigo1 = get_server_status_code1(url)

    # 3
    codigo2 = get_server_status_code2(url)

    # Comprobar si existe un URL sin necesidad de descargar todo el archivo
    # JSON con la respuesta de todos los métodos aplicados
    return {'host': codigo, 'url1': codigo1, 'url2': str(codigo2)}
