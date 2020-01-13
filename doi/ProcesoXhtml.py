""""
Created on 02-12-2019

@author: FJSB

Genera lista de contenidos de la ruta

"""

from doi.ProcesoUrl import *

lista = []


# Generar lista de LINK y DOI
def generar_lista(ruta, parametros=''):

    global lista

    print('#######')
    print(' LISTA')
    print('#######')
    lista = []

    with open(ruta, 'r', encoding='utf8') as f:

        # Cuenta DOI
        n_doi = 0
        n_doi_r = 0
        # Cuenta LINKS
        n_links = 0
        n_links_r = 0
        
        lineas = f.readlines()

        for texto in lineas:
            #######################
            # Tratamiento AMPLIADO de TEXTO \[(data|link|twitgram|anonimo|movil|email)\]
            #######################

            #
            # HTML ENTITY
            #
            # Busca entidades y los sustituye por el carácter equivalente
            import html as html

            # texto = html.unescape('Hola, cuando se concrete la fecha para &#39;APP-III&#39;, me dices, por mi parte, si me avisas con tiempo mejor&iexcl;&iexcl;  Saludos&iexcl;&iexcl;')
            texto = html.unescape(texto)

            #
            # ADJUNTOS (DOCUMENTOS, IMAGENES o EMOTICONOS)
            #
            import re

            def tratamiento(item):
                print(item)
                return item

            ######################
            #       DOI
            ######################
            # Busca DOI (10.) y los reemplaza por ' [DOI] '
            # Regex para DOI1: \b(10[.][0-9]{4,}(?:[.][0-9]+)*/[a-zA-Z0-9._-]*)
            # Regex para DOI3: \b(10[.][0-9]{4,}(?:[.][0-9]+)*(/*[(a-z)(A-Z)(0-9)/:;%._-]*)*)
            if texto.find('10.') != -1:
                # Todos los doi
                n_doi = n_doi + len(re.findall(r'\b(10[.][0-9]{4,}(?:[.][0-9]+)*(/*[(a-z)A-Z0-9/:;%._-]*)*)', texto, re.M | re.I))
                print('DOI ENCONTRADAS: ', n_doi)
                
            # Busca DOI y los reemplaza por [DOI]
            # Busca DOI
            dois = re.findall(r'\b(10[.][0-9]{4,}(?:[.][0-9]+)*(/*[(a-z)A-Z0-9/:;%._-]*)*)', texto, re.M | re.I)
            # Cuenta DOI
            n_doi_r = len(re.findall(r'\b(10[.][0-9]{4,}(?:[.][0-9]+)*(/*[(a-z)A-Z0-9/:;%._-]*)*)', texto, re.M | re.I))
            
            if n_doi_r != 0:
                # Reemplaza todos los DOI por [DOI]
                texto = re.sub(r'\b(10[.][0-9]{4,}(?:[.][0-9]+)*(/*[()a-zA-Z0-9/:;%._-]*)*)', ' [DOI] ', texto)
                # print('DOI REEMPLAZADOS: ', n_doi_r, url, texto)
                
                # Probar DOI:
                for doi in dois:
                    # Construye DOI
                    url = 'https://dx.doi.org/' + doi[0]

                    error_url = check_url(url)
                    if error_url['host'] == 404 or error_url['url1'] == 'False' or error_url['url2'].find('404') != -1:
                        print('DOI URL (', n_doi, ') ERROR: ', error_url)
                        print('DOI ERRÓNEO: ', n_doi_r, url, texto)
                        lista.append({'TIPO': 'DOI', 'URI': url, 'N': n_doi})
                    else:
                        print('DOI OK.')

            ######################
            #       LINKS
            ######################
            # Busca LINKS y los reemplaza por ' [LINK] '
            if texto.find('http') != -1:
                # Todos los http
                n_links = n_links + len(re.findall(r'(http)', texto, re.M | re.I))
                print('LINKS ENCONTRADOS: ', n_links)

            # Busca links y los reemplaza por [LINK]
            # Regex para LINK: (?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’]))
            # Busca LINK
            links = re.findall(r'''(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’]))''', texto, re.M | re.I)
            # Cuenta LINK
            n_links_r = len(re.findall(r'''(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’]))''', texto, re.M | re.I))
            
            if n_links_r != 0:
                # Reemplaza todos los LINKS (http) (sin ADJUNTOS y EMOJIS)
                texto = re.sub(r'''(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’]))''', ' [LINK] ', texto)
                # print('LINKS REEMPLAZADOS: ', n_links_r, texto)

                # Probar LINKS:
                for link in links:
                    error_url = check_url(link[0])
                    if error_url['host'] == 404 or error_url['url1'] == 'False' or error_url['url2'].find('404') != -1:
                        print('LINK URL (', n_links, ') ERROR: ', error_url)
                        print('LINK ERRÓNEO: ', n_links_r, link[0], texto)
                        lista.append({'TIPO': 'LINK', 'URI': link[0], 'N': n_links})
                    else:
                        print('URL OK.')

            ######################
            # Busca archivos Adjuntos y enlaces
            # Cuenta IMAGENES: las <IMG '' .../>
            imagenes = re.findall(r'(\<img \'\'.*\\\>)', texto, re.M | re.I)
            n_adjs = len(imagenes)
            t_adj = 0
            if n_adjs > 0:
                for imagen in imagenes:
                    t_adj = t_adj + len(imagen)
            else:
                t_adj = 0  # '(0KB <IMG '' .../>)'

            # Cuenta EMOJI: las <IMG '.+' .../>
            n_emojis = len(re.findall(r'(\<img \'.+\'.*\\\>)', texto, re.M | re.I))
            if n_emojis > 0:
                print()
                # print('EMOJIS:', n_emojis)

            # Busca ADJUNTOS Y EMOJIS y los reemplaza por [DATA]
            if texto.find('[IMAGE:') != -1:
                # print('ADJUNTOS ENCONTRADOS: ', n_adjs)
                # Busca [IMAGE:
                regex = re.search(r'(\[IMAGE: .*\])', texto, re.M | re.I)
                if regex != None:
                    # Reemplaza todos los ADJUNTOS Y EMOJIS [IMAGE:] por [DATA] Ampliación: poner tipo [DATA:XXX]
                    texto = re.sub(r'(\[IMAGE: .*\])', ' [DATA] ', texto)
                    # print(regex.group(1))
                    # print(texto)
                    # exit(12345567890)

            # Busca LINKS (ya eliminados ADJUNTOS y EMOJIS)
            if texto.find('http') != -1:
                # Todos los http
                n_links = len(re.findall(r'(http)', texto, re.M | re.I))
                # print('LINKS ENCONTRADOS: ', n_links)

            # Busca links y los reemplaza por [LINK]
            # Regex para DOI: \b(10[.][0-9]{4,}(?:[.][0-9]+)*/[a-zA-Z0-9._-]*)
            n_links_r = len(re.findall(
                r'''(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’]))''',
                texto, re.M | re.I))
            if n_links_r != 0:
                # Reemplaza todos los LINKS (http) (sin ADJUNTOS y EMOJIS)
                texto = re.sub(
                    r'''(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’]))''',
                    ' [LINK] ', texto)
                # print('LINKS REEMPLAZADOS: ', n_links_r, texto)

            # Cuenta ARROBAS, HASHTAG Y MOVILES
            n_arrobas = 0
            n_emails_r = 0
            n_twiters_r = 0
            n_hashtags = 0
            n_hashtagr_r = 0
            n_moviles = 0
            n_moviles_r = 0
            n_abrev = 0
            n_abrev_r = 0

            # Busca ARROBAS y los reemplaza por [EMAIL] o [TWITGRAM]
            if texto.find('@') != -1:
                # Todos los email, twitter o telegram id
                n_arrobas = len(re.findall(r'(@)', texto, re.M | re.I))
                # print('ARROBAS ENCONTRADAS: ', n_arrobas)
            # Busca EMAILS y los reemplaza por [EMAIL]
            n_emails_r = len(re.findall(r'([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)', texto, re.M | re.I))
            if n_emails_r != 0:
                # Reemplaza todos los EMAILS (a@a.a) (sin LINKS, ADJUNTOS y EMOJIS)
                texto = re.sub(r'([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)', ' [EMAIL] ', texto)
                # print('EMAILS REEMPLAZADOS: ', n_emails_r, texto)
            # Busca TWITTER/TELEGRAM ID (@a) y los reemplaza por ' [TWITGRAM] '
            n_twitters_r = len(re.findall(r'(^|[^@\w])@(\w{1,15})\b', texto, re.M | re.I))
            if n_twitters_r != 0:
                # Reemplaza todos los TWITTER/TELEGRAMS ID (@a) (sin EMAILS, LINKS, ADJUNTOS y EMOJIS)
                texto = re.sub(r'(^|[^@\w])@(\w{1,15})\b', ' [TWITGRAM] ', texto)
                # print('TWITTER/TELEGRAM ID REEMPLAZADOS: ', n_twitters_r, texto)

            # Busca HASHTAGS (#) y los reemplaza por ' [HASHTAG] '
            # r'#(\w+)'
            if texto.find('#') != -1:
                # Todos los hashtags
                n_hashtags = len(re.findall(r'(#)', texto, re.M | re.I))
                # print('HASHTAGS ENCONTRADAS: ', n_hashtags)
            # Busca HASHTAGS ID y los reemplaza por [HASHTAG]
            n_hashtags_r = len(re.findall(r'(^|[^#\w])#(\w{1,15})\b', texto, re.M | re.I))
            if n_hashtags_r != 0:
                # Reemplaza todos los HASHTAGS (#a) (sin TWITTER/TELEGRAMS, EMAILS, LINKS, ADJUNTOS y EMOJIS)
                texto = re.sub(r'(^|[^#\w])#(\w{1,15})\b', ' [HASHTAG] ', texto)
                # print('HASHTAGS REEMPLAZADOS: ', n_hashtags_r, texto)

            # Busca NUMEROS DE MOVIL y los reemplaza por ' [MOVIL] ' DE LOS GRUPOS DE TELEGRAM/WHATSAPP
            # r'(\+34|0034|34)?[ -.]*(6|7)[ -.]*([0-9][ -.]*){8}'
            if texto.find('6') != -1 or texto.find('7') != -1:
                # Todos los móviles
                n_moviles = len(re.findall(r'(\+34|0034|34)?[ -.]*(6|7)[ -.]*([0-9][ -.]*){8}', texto, re.M | re.I))
                # print('MOVILES ENCONTRADOS: ', n_moviles)
            # Busca MOVILES y los reemplaza por [MOVIL]
            n_moviles_r = len(re.findall(r'(\+34|0034|34)?[ -.]*(6|7)[ -.]*([0-9][ -.]*){8}', texto, re.M | re.I))
            if n_moviles_r != 0:
                # Reemplaza todos los MOVILES (#a) (sin HASHTAGS, TWITTER/TELEGRAMS, EMAILS, LINKS, ADJUNTOS y EMOJIS)
                texto = re.sub(r'(\+34|0034|34)?[ -.]*(6|7)[ -.]*([0-9][ -.]*){8}', ' [MOVIL] ', texto)
                # print('MOVILES REEMPLAZADOS: ', n_moviles_r, texto)

            #
            # ABREVIATURAS DE NOMBRES
            #
            # Busca nombres y los sustituye por ' [ANONIMO] '

            # Busca Abreviaturas Nombres Mª, Mª., M.ª, Fco, Fco.
            #                    Apellidos Gª, Gª., G.ª
            #  y los reemplaza por ' ANONIMO ' ' Maria ' ' Francisco ' ' Garcia '
            if texto.find('Mª') != -1 or texto.find('Mª.') != -1 or texto.find('M.ª') != -1 or texto.find('Gª') != -1 or texto.find('Gª.') != -1 or texto.find('G.ª') != -1:
                # or texto.find('Fco') != -1 or texto.find('Fco.') != -1 or texto.find('Fco') != -1:
                # Todas las abreviaturas
                n_abrev = len(re.findall(r'(M|m|G|g)[ .]*ª[ .]*', texto, re.M | re.I))
                # print('ABREVIATURAS ENCONTRADAS: ', n_abrev)
            # Busca ABREVIATURAS y las reemplaza por ' [ANONIMO] '
            n_abrev_r = len(re.findall(r'(M|m|G|g)[ .]*ª[ .]*', texto, re.M | re.I))
            if n_abrev_r != 0:
                # Reemplaza todos las ABREVIATURAS
                texto = re.sub(r'(M|m|G|g)[ .]*ª[ .]*', ' [ANONIMO] ', texto)
                # print('ABREVIATURAS REEMPLAZADAS: ', n_abrev_r, texto)

            #######################
            # FIN Tratamiento AMPLIADO de TEXTO \[(data|link|twitgram|anonimo|movil|email)\]
            #######################

    return lista
