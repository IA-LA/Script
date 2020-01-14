"""Este fichero contiene las siguientes clases:
    - ExtensionSpider: la spider que se encarga de lanzar requests y extraer los datos de las responses.
    - ExtensionItem: una clase para identificar los campos de los ítems que queremos extraer.
    - ExtensionPipeline: un pipeline que sirve para poder manejar los objetos que se recuperan.
"""

import scrapy
from bs4 import BeautifulSoup
from urllib.parse import urlencode
import json


class ExtensionSpider(scrapy.Spider):
    """Los objetos de tipo Spider en scrapy sirven para guiar el scraping de un conjunto de páginas
    https://docs.scrapy.org/en/latest/topics/spiders.html
    """

    # Le damos un nombre a la spider para poder ser referida en una nueva sesión de crawling
    name = "extension_spider"

    # La clase Spider en scrapy tiene un atributo con nombre "start_urls" que se emplea por defecto
    # para establecer la/las urls de partida.
    start_urls = ["https://extension.uned.es/"]

    # La clase Spider en scrapy, cuando se ejecuta dentro de una sesión de crawling, ejecuta por defecto
    # el método con nombre "start_requests". Este método, si no se sobreescribe, descarga todas las urls
    # incluidas en start_urls y realiza la extracción indicada por el método con nombre "parse".

    # En este caso no hace falta definirlo, pues sólo tenemos una url de partida. Pero si es necesario se reescribe:
    # def start_requests(self):
    #   Por cada request:
    #       yield scrapy.Request(url=url_request, callback=self.parse) # ó callback = metodo que quieras

    def parse(self, response):
        """ El método por defecto para procesar las requests es el que tiene el nombre 'parse'.
        Este es el método que se encargará de procesar la página principal"""

        # Recupero el cuerpo de la respuesta y lo abro con BeautifulSoup:
        html = BeautifulSoup(response.body_as_unicode(), "html5lib")
        elementos_actividad = html.find_all("div", {"class": "actividad"})

        # Recupero los campos de cada actividad
        for i, elemento in enumerate(elementos_actividad):
            nombre_elemento = elemento.find("div", {"class": "titulo"}).get_text().strip()
            centro_elemento = elemento.find("a", {"class": "centro"}).get_text().strip()
            enlace_elemento = elemento.find("div", {"class": "titulo"}).a["href"]

            # El id son los números que aparecen después de la última ocurrencia del caracter "/":
            id_actividad = enlace_elemento[enlace_elemento.rfind("/")+1:]

            # Genero un nevo ExtensionItem con los datos recopilados hasta ahora
            item = ExtensionItem({"nombre": nombre_elemento, "id": id_actividad, "centro": centro_elemento})

            # Finalmente indico que el scrapeo sigue en la página individual de la actividad
            # Para ello, indico la nueva url a descargar, el ítem de datos hasta ahora, y el nuevo método de parsing
            # para la nueva url
            url_pagina_individual = "https://extension.uned.es/" + enlace_elemento[1:]
            yield scrapy.Request(url_pagina_individual, callback=self.parse_individual, meta={'item': item})

    def parse_individual(self, response):
        """Este es el método que scrapea información sobre la página individual de cada evento/actividad"""

        # Recupero lo que llevo hasta ahora de ítem recopilado
        item = response.meta['item']

        # Proceso el html de la nueva página descargada
        html = BeautifulSoup(response.body_as_unicode(), "html5lib")
        actividad = html.find("div",{"id": "principal"}).find("dl", {"id": "actividad"}).find("dl", recursive=False)
        # print(actividad)
        hijos = actividad.find_all(recursive=False)
        for i, hijo in enumerate(hijos):
            if "Dirigido por" == hijo.get_text().strip():
                nombre_director = hijos[i+1].find("dl",{"id":"ponencias"}).\
                    find("",{"itemprop":"name"}).get_text().strip()
                item.update({"director":nombre_director})
        yield item


class ExtensionPipeline(object):
    """ Los objetos tipo pipeline sirven para hacer post-procesado de los datos extraídos.
    En una sesión de crawling, se incluirá este pipeline en configuración para que los objetos extraídos
    por ExtensionSpider sean post-procesados aquí. Una típica operación de post-procesado es su almacenamiento
    en una BBDD. La ventaja de separar el post-procesado de la extracción es que se hace asíncrono y por eso más veloz.
    https://docs.scrapy.org/en/latest/topics/item-pipeline.html
    """

    # Para que un pipeline pueda ser usado en scrapy, este tiene que ser cualquier clase (por eso hereda de object)
    # y tener implementado el método con nombre "process_item"
    def process_item(self, item, spider):

        # Tengo acceso a la spider que ha generado el ítem, en este caso sólo hay una spider, así que lo siguiente
        # no es necesario
        # if spider.name == "entity_linking":
        # print("ITEM EN PIPELINE : ", item)
        json_item = json.dumps(item.__dict__, ensure_ascii=False)
        print("JSON : ", json_item)
        # Aqui podrias almacenar el json en una bd o hacer append en un fichero
        return


class ExtensionItem(scrapy.Item):
    """Este es el modelo de datos de tus ítems
    https://docs.scrapy.org/en/latest/topics/items.html#declaring-items
    """
    nombre = scrapy.Field()
    id = scrapy.Field()
    centro = scrapy.Field()
    director = scrapy.Field()
