# coding= utf-8
'''Created on 20/03/2015

@author: felipexw
'''
from django.http.response import HttpResponse
from django.shortcuts import render
from main_controller import get_feed, get_coments, get_user_info
import math
ACCESS_TOKEN = 'CAACEdEose0cBANKkCXCmBQYBIToVSq2yP5UTVkQEWxrmNHZBT2iZBnGo4YLGWmWn3qo5uLXtE0EZBf4WMA3lxFARMDUdH9k6gXYlnVxlpFn5o7SyyIydXfmPJgnLle6rYrI71QzbV1aaVk5D4bolIuSsbY7DNn5IFgcT426S4pjrh2qIxd1ntzcjZC2Ceyl2wDjoC7tKUSejBicZB6lKk'
user_info = {}


def show_posts(request):
    numero_pagina = request.GET.get('page')
    quantidade_comentarios_pagina = 5
    
    if  numero_pagina == None:
        numero_pagina = 1
    
    html = '<div class="container theme-showcase" role="main"> <div class="row">  <div class="bs-example" data-example-id="panel-without-body-with-table"> <div class="panel panel-default"> <div class="panel-heading"> Publicacoes no Facebook </div> <table class="table table-stripped"> <thead>  <tr> <th colspan="1"> Usuario </th> <th> Post</th> <th> Link </th> <th> Acao </th> </tr> </thead> <tbody id="tbody_conteudo">'
    dados = get_feed(ACCESS_TOKEN)
    user_info = get_user_info(ACCESS_TOKEN)
    
    ultimo_indice = (quantidade_comentarios_pagina * int(numero_pagina)) 
    primeiro_indice = ultimo_indice - quantidade_comentarios_pagina
    
    j = 0
    
    for i in xrange(0, len(dados)):
        if i >= primeiro_indice and i < ultimo_indice:
            if dados[i]['mensagem'] == '':
                dados[i]['mensagem'] = '(Publicacao sem texto)'
            html += '<tr><td colspan="1">' + dados[i]['autor'] + '</td><td>' + dados[i]['mensagem'] + '</td><td><a href="%s' % dados[i]['link'] + '">Link</a></td><td><a href='"comments?id=" + dados[i]['id'] + '' + ' role="button" class="btn btn-sm btn-success">Analizar</a></td></tr>'
            j += 1
        if j == quantidade_comentarios_pagina:
            break        
    html += ' <tbody id="tbody_conteudo"> </tbody> </table> </div> </div> '                        
    html += get_html_paginacao(len(dados))
    return render(request, 'base.html', {'name': user_info.get('sobrenome'), 'conteudo_dinamico': html})

def get_html_paginacao(tamanho, quantidade_comentarios = 5):
    html = '<ul class="pagination pagination-lg">'
    
    limite = int(math.ceil(tamanho/quantidade_comentarios)) 
    for i in xrange(0, limite):
        html += '<li><a href="posts?page=%i' % int(i+1) + '">%i' % int(i+1) + '</a></li>'
        
    html += '</ul>'
    return html    

def show_home(request):
    html = '<div class="jumbotron"> <h1>Seja bem-vindo ao Guessb!</h1><p>Este webapp é o Trabalho de Conclusão de Curso (TCC) do Felipe Appio. Seu objetivo é fazer análise de sentimentos em comentários e publicações do Facebook.</p> <p></div></div>'
    return render(request, 'base.html', {'conteudo_dinamico':html})


def get_comentarios(request):
    html = '<div class="container theme-showcase" role="main"> <div class="row"> <div class="bs-example" data-example-id="panel-without-body-with-table"> <div class="panel panel-default"> <div class="panel-heading"> Publicacoes no Facebook </div> <table class="table table-stripped"> <thead>  <tr> <th colspan="1"> Usuario </th> <th> Post</th> <th> Acao </th> </tr> </thead> <tbody id="tbody_conteudo">'
 
    comentarios = get_coments(ACCESS_TOKEN, request.GET.get('id'))
    for comentario in comentarios:
        html += '<tr><td colspan="1">' + comentario['autor_comentario'] + '</td><td>' + comentario['comentario'] + '</td>' + '<td>' + comentario['polaridade'] + '</td></tr>'

    html += '</tbody></table>'                        
    return render(request, 'base.html', {'name': user_info.get('sobrenome'), 'conteudo_dinamico': html})


def show_paginacao(request):
    return render(request, 'paginacao.html', {})

