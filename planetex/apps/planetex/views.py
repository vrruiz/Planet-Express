# -*- encoding: utf-8 -*-
# Create your views here.
from django.core.extensions import get_object_or_404, render_to_response
from django.core.template import loader
from django.models.planetex import feeds, posts
from django.utils.httpwrappers import HttpResponse
from django.utils.html import strip_tags

def index(request):
    import datetime
    feed_list = feeds.get_list(feed_type__exact='planet', order_by=['title'])
    post_list = posts.get_list(feed__feed_type__exact='planet', order_by=['-modified'], limit=40)
    post_short_list = posts.get_list(feed__feed_type__exact='planet', modified__gt = (datetime.datetime.now() - datetime.timedelta(hours=24)), order_by=['-modified'], offset=41, limit=100)
    delicious_list = posts.get_list(feed__feed_type__exact='delicious', order_by=['-modified'], limit=20)
    return render_to_response('planetex/index', {'feeds':feed_list, 'posts':post_list, 'posts_short':post_short_list, 'delicious':delicious_list})

def atom(request):
    feed_list = feeds.get_list(feed_type__exact='planet', order_by=['title'])
    post_list = posts.get_list(order_by=['-modified'], limit=40)
    content = loader.render_to_string('planetex/atom', {'feeds':feed_list, 'posts':post_list})
    return HttpResponse(content, mimetype='text/xml')

def opml(request):
    import datetime
    feed_list = feeds.get_list(feed_type__exact='planet', order_by=['title'])
    content = loader.render_to_string('planetex/opml', {'feeds':feed_list, 'date_created':datetime.datetime.now()})
    return HttpResponse(content, mimetype='text/xml')
    

def wordcloud(request):
    stop_words = ['un', 'una', 'unas', 'unos', 'uno', 'sobre', 'todo', 'también', 'tras', 'otro', 'algún', 'alguno', 'alguna', 'algunos', 'algunas', 'ser', 'es', 'soy', 'eres', 'somos', 'sois', 'estoy', 'esta', 'estamos', 'estais', 'estan', 'como', 'en', 'para', 'atras', 'porque', 'por qué', 'estado', 'estaba', 'ante', 'antes', 'siendo', 'ambos', 'pero', 'por', 'poder', 'puede', 'puedo', 'podemos', 'podeis', 'pueden', 'fui', 'fue', 'fuimos', 'fueron', 'hacer', 'hago', 'hace', 'hacemos', 'haceis', 'hacen', 'cada', 'fin', 'incluso', 'primero', 'desde', 'conseguir', 'consigo', 'consigue', 'consigues', 'conseguimos', 'consiguen', 'ir', 'voy', 'va', 'vamos', 'vais', 'van', 'vaya', 'gueno', 'ha', 'tener', 'tengo', 'tiene', 'tenemos', 'teneis', 'tienen', 'el', 'la', 'lo', 'las', 'los', 'su', 'aqui', 'mio', 'tuyo', 'ellos', 'ellas', 'nos', 'nosotros', 'vosotros', 'vosotras', 'si', 'dentro', 'solo', 'solamente', 'saber', 'sabes', 'sabe', 'sabemos', 'sabeis', 'saben', 'ultimo', 'largo', 'bastante', 'haces', 'muchos', 'aquellos', 'aquellas', 'sus', 'entonces', 'tiempo', 'verdad', 'verdadero', 'verdadera   cierto', 'ciertos', 'cierta', 'ciertas', 'intentar', 'intento', 'intenta', 'intentas', 'intentamos', 'intentais', 'intentan', 'dos', 'bajo', 'arriba', 'encima', 'usar', 'uso', 'usas', 'usa', 'usamos', 'usais', 'usan', 'emplear', 'empleo', 'empleas', 'emplean', 'ampleamos', 'empleais', 'valor', 'muy', 'era', 'eras', 'eramos', 'eran', 'modo', 'bien', 'cual', 'cuando', 'donde', 'mientras', 'quien', 'con', 'entre', 'sin', 'trabajo', 'trabajar', 'trabajas', 'trabaja', 'trabajamos', 'trabajais', 'trabajan', 'podria', 'podrias', 'podriamos', 'podrian', 'podriais', 'yo', 'aquel', 'i', 'a', 'about', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'com', 'de', 'en', 'for', 'from', 'how', 'in', 'is', 'it', 'la', 'of', 'on', 'or', 'that', 'the', 'this', 'to', 'was', 'what', 'when', 'where', 'who', 'will', 'with', 'und', 'the', 'www', 'alors', 'au', 'aucuns', 'aussi', 'autre', 'avant', 'avec', 'avoir', 'bon', 'car', 'ce', 'cela', 'ces', 'ceux', 'chaque', 'ci', 'comme', 'comment', 'dans', 'des', 'du', 'dedans', 'dehors', 'depuis', 'deux', 'devrait', 'doit', 'donc', 'dos', 'droite', 'début', 'elle', 'elles', 'en', 'encore', 'essai', 'est', 'et', 'eu', 'fait', 'faites', 'fois', 'font', 'force', 'haut', 'hors', 'ici', 'il', 'ils', 'je','juste', 'la', 'le', 'les', 'leur', 'là', 'ma', 'maintenant', 'mais', 'mes', 'mine', 'moins', 'mon', 'mot', 'même', 'ni', 'nommés', 'notre', 'nous', 'nouveaux', 'ou', 'où', 'par', 'parce', 'parole', 'pas', 'personnes', 'peut', 'peu', 'pièce', 'plupart', 'pour', 'pourquoi', 'quand', 'que', 'quel', 'quelle', 'quelles', 'quels', 'qui', 'sa', 'sans', 'ses', 'seulement', 'si', 'sien', 'son', 'sont', 'sous', 'soyez   sujet', 'sur', 'ta', 'tandis', 'tellement', 'tels', 'tes', 'ton', 'tous', 'tout', 'trop', 'très', 'tu', 'valeur', 'voie', 'voient', 'vont', 'votre', 'vous', 'vu', 'ça', 'étaient', 'état', 'étions', 'été', 'être']
    import re
    post_list = posts.get_iterator(limit=100)
    word_count=dict()
    for post in post_list:
        words = re.sub('(?u)\W|\d', ' ', strip_tags(post.content)).split(' ')
        for word in words:
            if (word.lower() in stop_words):
                continue
            if (word_count.has_key(word)):
                word_count[word] = word_count[word] + 1
            else:
                word_count[word] = 1
    words = word_count.keys()
    words.sort()
    content = ''
    for word in words:
        if (word_count[word] > 5):
            content = content + '<font size=+%s>%s</font> ' % (word_count[word] - 15, word)
    return HttpResponse(content)