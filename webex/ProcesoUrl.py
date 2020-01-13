""""
Created on 03-12-2019

@author: FJSB

Opciones de verificación de URL

"""

import http.client
import urllib.parse
import urllib.request
from bs4 import BeautifulSoup
import re

web_extension = 'http://extension.uned.es'


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


# funcion que se encarga de obtener respuesta del estatus del servidor web
# URLLIB.REQUEST
def get_url(url):
    print('GET URL')
    try:
        contents = urllib.request.urlopen(url).read()
        page = urllib.request.urlopen(url)
        soup = BeautifulSoup(page, "html5lib")
        print('CONTENIDOS:', contents)
        print('PAGINA:', page)

        # Título
        titulo = soup.title.string
        print('TITULO:', titulo)
        # print('PARSE:', soup.div(id='contenedor_central'))
        # print('PARSE:', soup.div(id='principal'))
        # print('PARSE:', soup.div(id='fecha_creditos'))
        # Fecha
        fecha = soup.div(id='fecha_actividad')
        print('FECHA:', fecha)
        # Tipo
        tipo = soup.div(id='online')
        print('TIPO:', tipo)
        # Centro
        centro = soup.div(id='centro')
        print('CENTRO:', centro)

        # Ponentes
        ponentes = soup.find_all(['a'], href=re.compile('idponente'))
        print('PONENTES:', ponentes)

        exit(0)

        print('PARSE:', soup.div(id='actividad'))
        print('PARSE0:', soup.find_all(['div'], attrs={"class": "contenedor_actividad"}))
        print('PARSE0:', soup.find_all(['div'], attrs={"class": 'cabeceraDetalleActividad'}))
        print('PARSE0:', soup.find_all(['div'], attrs={"class": 'cajasActividad'}))
        #print('PARSE LIMPIO:', soup.prettify())

        return soup.title.string
    except Exception as e:
        return e


# funcion que se encarga de obtener respuesta del estatus del servidor web
# URLLIB.REQUEST
def get_url_curso(url):
    print('     GET URL CURSO')
    print('     #############')
    try:
        contents = urllib.request.urlopen(url).read()
        page = urllib.request.urlopen(url)
        soup = BeautifulSoup(page, "html5lib")
        print('     CONTENIDOS:', contents)
        print('     PAGINA:', page)

        # Título
        titulo = soup.title.string
        print('     TITULO:', titulo)
        # print('PARSE:', soup.div(id='contenedor_central'))
        # print('PARSE:', soup.div(id='principal'))
        # print('PARSE:', soup.div(id='fecha_creditos'))
        # Fecha
        fecha = soup.div(id='fecha_actividad')
        print('     FECHA:', fecha)
        # Tipo
        tipo = soup.div(id='online')
        print('     TIPO:', tipo)
        # Centro
        centro = soup.div(id='centro')
        print('     CENTRO:', centro)

        # Archivos
        archivos = soup.find_all(['a'], href=re.compile('archivos_publicos/webex_actividades'))
        print('     ARCHIVOS:', archivos)

        # Ponentes
        ponentes = soup.find_all(['a'], href=re.compile('idponente'))
        print('     PONENTES:', ponentes)

        # print('PARSE:', soup.div(id='actividad'))
        # print('PARSE0:', soup.find_all(['div'], attrs={"class": "contenedor_actividad"}))
        # print('PARSE0:', soup.find_all(['div'], attrs={"class": 'cabeceraDetalleActividad'}))
        # print('PARSE0:', soup.find_all(['div'], attrs={"class": 'cajasActividad'}))
        # print('PARSE LIMPIO:', soup.prettify())

        return soup.title.string
    except Exception as e:
        return e


# funcion que se encarga de obtener respuesta del estatus del servidor web
# URLLIB.REQUEST
def get_url_actividades(url):
    print('GET URL ACTIVIDADES')
    print('###################')
    try:
        contents = urllib.request.urlopen(url).read()
        page = urllib.request.urlopen(url)
        soup = BeautifulSoup(page, "html5lib")
        print('CONTENIDOS:', contents)
        print('PAGINA:', page)

        # Título
        titulo = soup.title.string
        print('TITULO:', titulo)
        # print('PARSE:', soup.div(id='contenedor_central'))
        # print('PARSE:', soup.div(id='principal'))
        # print('PARSE:', soup.div(id='fecha_creditos'))

        # Actividades
        actividades = soup.find_all(['a'], href=re.compile('actividad/idactividad'))
        #print('ACTIVIDADES:', actividades)
        for actividad in actividades:
            # ID actividad
            link = actividad.get('href')
            idregistro = actividad.get('href').split('/')[3]
            # Actividad
            titulo = actividad.get_text()
            print('ACTIVIDAD:', idregistro, titulo, link)

            # DIV actividad
            actividad_completa = soup.find(['div'], idregistro=re.compile(idregistro))
            # Fecha
            fecha = "'Sólo disponible en los tres primeros cursos del listado'"
            print('FECHA:', fecha)
            # Tipo
            tipo = "'Sólo disponible en los tres primeros cursos del listado'"
            print('TIPO:', tipo)
            # Centro
            centro = actividad_completa.find(['a'], href=re.compile('indice/idcentro'))  # actividad.find_all(['a'], href=re.compile('indice/idcentro'))
            centro = centro.get_text()
            print('CENTRO:', centro)

            # WEB CURSO
            get_url_curso(web_extension + link)

        print('PARSE0:', soup.find_all(['div'], attrs={"class": "lista_mas_actividades"}))

        exit(0)

        print('PARSE:', soup.div(id='actividad'))
        print('PARSE0:', soup.find_all(['div'], attrs={"class": "contenedor_actividad"}))
        print('PARSE0:', soup.find_all(['div'], attrs={"class": 'cabeceraDetalleActividad'}))
        print('PARSE0:', soup.find_all(['div'], attrs={"class": 'cajasActividad'}))
        #print('PARSE LIMPIO:', soup.prettify())

        return soup.title.string
    except Exception as e:
        return e
