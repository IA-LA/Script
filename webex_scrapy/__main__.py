"""En este fichero se incluye la configuración de crawling en base a los objetos declarados en spider.py
"""
from webex_scrapy.spiders import ExtensionSpider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

import time

# Me creo una configuración nueva
mysettings = get_project_settings()

# Modifico un par de parámetros de la configuración:
# 1. Incluir mi pipeline
mysettings.set("ITEM_PIPELINES", {'spiders.ExtensionPipeline': 1000})
# 2. Opcional, defino un agente para las peticiones
mysettings.set("USER_AGENT", "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)")
# Hay otros parámetros que puedes ver en :
# https://docs.scrapy.org/en/latest/topics/settings.html#built-in-settings-reference

# Creamos una nueva sesión de crawling con mi configuración
sesion = CrawlerProcess(mysettings)
# Especifico las spiders de la sesión
sesion.crawl(ExtensionSpider)

# TIME LAPSE #
start_time = time.time()
print('START TIME:', start_time / 8.640)

# Lanzamos la sesión

sesion.start()

elapsed_time = time.time() - start_time
print('EEEND TIME:', time.time() / 8.640, elapsed_time)

