# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para piratestreaming
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os, sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

__channel__ = "cineblogfm"
__category__ = "F,S"
__type__ = "generic"
__title__ = "CineBlog01.FM"
__language__ = "IT"

sito="http://www.cineblog01.fm"

DEBUG = config.get_setting("debug")

def isGeneric():
    return True

def mainlist(item):
    logger.info("pelisalacarta.cineblogfm mainlist")
    itemlist = []
    itemlist.append( Item(channel=__channel__, title="Nuovi Film", action="peliculas", url=sito+"/new-film-streaming/"))
    itemlist.append( Item(channel=__channel__, title="Serie TV", action="peliculas", url=sito+"/telefilm-serie-tv-streaming/"))
    itemlist.append( Item(channel=__channel__, title="Film Per Genere", action="categorias", url=sito))
    itemlist.append( Item(channel=__channel__, title="Film Per Paese", action="catpays", url=sito))
    itemlist.append( Item(channel=__channel__, title="Film Per Anno", action="catyear", url=sito))
    #itemlist.append( Item(channel=__channel__, title="Film e Serie per anno", action="byyear", url="http://filmstream.pw/"))
    #itemlist.append( Item(channel=__channel__, title="Serie TV", action="peliculas", url="http://filmstream.pw/serie-tv/"))
    itemlist.append( Item(channel=__channel__, title="Cerca...", action="search"))

    
    return itemlist

def categorias(item):
    logger.info("pelisalacarta.cineblogfm categorias")
    itemlist = []
    
    data = scrapertools.cache_page(item.url)
    logger.info(data)

    # Narrow search by selecting only the combo
    bloque = scrapertools.get_match(data,'<li class="drop"><a href="/" class="link1"><b>Film Streaming </b></a>.*?<ul>(.*?)<li class="drop">')
    
    # The categories are the options for the combo
    patron = '<li><a href="(.*?)">(.*?)</a></li>'
    matches = re.compile(patron,re.DOTALL).findall(bloque)
    scrapertools.printMatches(matches)

    for url,titulo in matches:
        scrapedtitle = titulo
        scrapedurl = urlparse.urljoin(item.url,url)
        scrapedthumbnail = ""
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=__channel__, action="peliculas" , title=scrapedtitle , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot))

    return itemlist

def catpays(item):
    logger.info("pelisalacarta.cineblogfm categorias")
    itemlist = []
    
    data = scrapertools.cache_page(item.url)
    logger.info(data)

    # Narrow search by selecting only the combo
    bloque = scrapertools.get_match(data,'<li class="drop"><a href="/" class="link1"><b>Film per paese</b></a>(.*?)<li class="drop">')
    
    # The categories are the options for the combo
    patron = '<li><a.*?href="(.*?)">(.*?)</a></li>'
    matches = re.compile(patron,re.DOTALL).findall(bloque)
    scrapertools.printMatches(matches)

    for url,titulo in matches:
        scrapedtitle = titulo
        scrapedurl = urlparse.urljoin(item.url,url)
        scrapedthumbnail = ""
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=__channel__, action="peliculas" , title=scrapedtitle , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot, folder=True ))

    return itemlist

def catyear(item):
    logger.info("pelisalacarta.cineblogfm categorias")
    itemlist = []
    
    data = scrapertools.cache_page(item.url)
    logger.info(data)

    # Narrow search by selecting only the combo
    bloque = scrapertools.get_match(data,'<li class="drop"><a href="/" class="link1"><b>Film per anno</b></a>(.*?)<li class="drop">')
    
    # The categories are the options for the combo
    patron = '<li><a.*?href="(.*?)">(.*?)</a></li>'
    matches = re.compile(patron,re.DOTALL).findall(bloque)
    scrapertools.printMatches(matches)

    for url,titulo in matches:
        scrapedtitle = titulo
        scrapedurl = urlparse.urljoin(item.url,url)
        scrapedthumbnail = ""
        scrapedplot = ""
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=__channel__, action="peliculas" , title=scrapedtitle , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot, folder=True ))

    return itemlist

def search(item,texto):
    logger.info("[itafilmtv.py] "+item.url+" search "+texto)
    item.url = "http://www.cineblog01.fm/xfsearch/" + texto
    try:
        return peliculas(item)
    # Se captura la excepción, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error( "%s" % line )
        return []

def peliculas(item):
    logger.info("pelisalacarta.cineblogfm peliculas")
    itemlist = []

    # Descarga la pagina
    data = scrapertools.cache_page(item.url)

    # Extrae las entradas (carpetas)
    patron = '<div class="short-story">.*?<a href="(.*?)" title="(.*?)">.*?<img.*?style="background:url[^h]+(.*?)\) no-repeat'
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for scrapedurl,scrapedtitle,scrapedthumbnail in matches:
        response = urllib2.urlopen(scrapedurl)
        html = response.read()
        start = html.find("<div class=\"post-title\">")
        end = html.find("<td class=\"full-right\">", start)
        scrapedplot = html[start:end]
        scrapedplot = re.sub(r'<.*?>', '', scrapedplot)
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
        itemlist.append( Item(channel=__channel__, action="findvideos", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , folder=True) )


    # Extrae el paginador
    patronvideos  = '<span class="nav_ext">...</span> <a href=.*?</a> <a href="(.*?)">Avanti</a></div></div>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    if len(matches)>0:
        scrapedurl = urlparse.urljoin(item.url,matches[0])
        itemlist.append( Item(channel=__channel__, action="peliculas", title="[COLOR orange]Avanti >>[/COLOR]" , url=scrapedurl , folder=True) )

    return itemlist

def test():
    from servers import servertools
    
    # mainlist
    mainlist_items = mainlist(Item())
    # Da por bueno el canal si alguno de los videos de "Novedades" devuelve mirrors
    novedades_items = peliculas(mainlist_items[0])
    bien = False
    for novedades_item in novedades_items:
        mirrors = servertools.find_video_items( item=novedades_item )
        if len(mirrors)>0:
            bien = True
            break

    return bien
