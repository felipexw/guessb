# coding=utf-8
'''Created on 20/03/2015

@author: felipexw
'''
from django.http.response import HttpResponse
from django.shortcuts import render
from main_controller import get_feed, get_coments, get_user_info

ACCESS_TOKEN = 'CAACEdEose0cBAH2cXvVnZCAl5HxOrsPPZBth4glHtZCGCu3oFEA3J9lOMv6FfEI8dNlUH4DmgjVIKTYwy9YQ9gZBInFnax45xGMvVWLZBKMh2du0ej5W0BZAE2lDtkFiu7XZCz2OTtPbGqDtaErCu7pYxep7qhZCU2kppETFtcP9tZAeVgOKunQWxpCRwMbkgp5JStYOzonLNrVsWpeytjRDs'
user_info = {}

def login_home(request):
    name = 'Felipe Appio'
    return render(request, 'login_twitter.html', {'name': name})

def hello(requet):
    return HttpResponse("Hello world")

def home(request):
    html = ''
    dados = get_feed(ACCESS_TOKEN)
    user_info = get_user_info(ACCESS_TOKEN)

    for conteudo in dados:
        html += '<tr><td colspan="1">'+conteudo['autor']+'</td><td>'+conteudo['mensagem']+'</td><td>'+conteudo['link']+'</td><td><a href='"comentarios?id="+conteudo['id']+'' +' role="button" class="btn btn-sm btn-success">Verificar</a></td></tr>'

    html += '</tbody></table></div>'                        
    return render(request, 'base.html', {'name': user_info.get('sobrenome'), 'conteudo': html})

def get_comentarios(request):
    html = ''
    print 'request.GET.get(id)' + request.GET.get('id') 
    comentarios = get_coments(ACCESS_TOKEN, request.GET.get('id'))
    for comentario in comentarios:
        html += '<tr><td colspan="1">'+comentario['autor_comentario']+'</td><td>'+comentario['comentario']+'</td><td>'+comentario['autor_comentario']+'</td><td>'+comentario['polaridade']+'</td></tr>'

    html += '</tbody></table></div>'                        
    return render(request, 'base.html', {'name': user_info.get('sobrenome'), 'conteudo': html})