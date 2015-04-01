# coding=utf-8
'''Created on 20/03/2015

@author: felipexw
'''
from django.http.response import HttpResponse
from django.shortcuts import render
from main_controller import get_feed, get_coments

ACCESS_TOKEN = 'CAACEdEose0cBABkb4gZAbldBG1pb8bvR73gkV9gyss1teZCQRhCZAq5lgeOeNDBWdqNSeURprBWGPjYpp2T45LBRyvUdnafrsUtATf5tnScI4cvHvGyhqlB1zsUTsL0daivZCxGRObZBAUY5LI3Ql3pNDbWxZBT3sg61CBI91mMAroN4CLYF1SD18sGXCO9xDcu6dWc46HDavaPvvvc7XM'

def login_home(request):
    name = 'Felipe Appio'
    return render(request, 'login_twitter.html', {'name': name})

def hello(requet):
    return HttpResponse("Hello world")

def home(request):
    name = 'Appio'
    html = ''
    dados = get_feed(ACCESS_TOKEN)
    for conteudo in dados:
        html += '<tr><td colspan="1">'+conteudo['autor']+'</td><td>'+conteudo['mensagem']+'</td><td>'+conteudo['link']+'</td><td><a href='"comentarios?id="+conteudo['id']+'' +' role="button" class="btn btn-sm btn-success">Verificar</a></td></tr>'

    html += '</tbody></table></div>'                        
    return render(request, 'base.html', {'name': name, 'conteudo': html})

def get_comentarios(request):
    name = 'Appio'
    html = ''
    print 'request.GET.get(id)' + request.GET.get('id') 
    comentarios = get_coments(ACCESS_TOKEN, request.GET.get('id'))
    for comentario in comentarios:
        html += '<tr><td colspan="1">'+comentario['autor_comentario']+'</td><td>'+comentario['comentario']+'</td><td>'+comentario['autor_comentario']+'</td><td>'+comentario['polaridade']+'</td></tr>'

    html += '</tbody></table></div>'                        
    return render(request, 'base.html', {'name': name, 'conteudo': html})