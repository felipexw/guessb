# coding= utf-8
'''Created on 20/03/2015

@author: felipexw
'''
from django.http.response import HttpResponse
from django.shortcuts import render
from main_controller import get_feed, get_coments, get_user_info

import math
ACCESS_TOKEN = 'CAACEdEose0cBAM3uF2citqVNidoZBBQaTEozYrj1837WlFJp1BlVpeyrSNCovEyZAD1sOBmZBUfqn4UIgCmkbjQiZAtNZA21TZASmKe6M5vX4n4fLHf1U5ZANUQ8ZAbCZCZBJWg4MuCMrX2MJlivqxpQyWvxk24slhOvPxJOVOTHTlu2zNNZCT0GPoFzbDKOHJE57u5aoDt516ceFd79PjNQCAT'
user_info = {}
QUANTIDADE_PUBLICACOES_PAGINA = 5

def show_sobre(request):
    html = '<div class="jumbotron"> <h1>Seja bem-vindo ao Guessb!</h1><p>Este webapp é o Trabalho de Conclusão apresentado ao Curso de Sistemas de Informação, da Universidade do Estado de Santa Catarina, como requisito parcial para obtenção do grau de Bacharel em Sistemas de Informação.</p></div></div>'
    return render(request, 'base.html', {'conteudo_dinamico':html}) 
    

def show_posts(request):
    numero_pagina = request.GET.get('page')
    
    if  numero_pagina == None:
        numero_pagina = 1
    
    html = '<div class="container theme-showcase" role="main"> <div class="row">  <div class="bs-example" data-example-id="panel-without-body-with-table"> <div class="panel panel-default"><div class="panel-heading"><div class="btn-group pull-right"><button type="button" class="btn btn-default dropdown-toggle" data-toggle="dropdown"><i class="glyphicon glyphicon-th icon-th"></i> <span class="caret"></span></button>    <ul class="dropdown-menu" role="menu">    <li><input type="checkbox" value="pos" onclick="filtrar(this);">Positivo</li>  <li><input type="checkbox" value="neg" onclick="filtrar(this);">Negativo</li>  <li><input type="checkbox"   value="neu" onclick="filtrar(this);" >NEUTROo</li></ul>    </div>   <h4>Publicacoes no Facebook</h4></div><table class="table table-stripped"> <thead>  <tr> <th colspan="1"> Usuario </th> <th> Post</th> <th> Link </th> <th> Acao </th> </tr> </thead> <tbody id="tbody_conteudo">'
    dados = get_feed(ACCESS_TOKEN)
    user_info = get_user_info(ACCESS_TOKEN)
    
    ultimo_indice = (QUANTIDADE_PUBLICACOES_PAGINA * int(numero_pagina)) 
    
    primeiro_indice = ultimo_indice - QUANTIDADE_PUBLICACOES_PAGINA
    
    j = 0
    
    for i in xrange(0, len(dados)):
        if i >= primeiro_indice and i < ultimo_indice:
            if dados[i]['mensagem'] == '':
                dados[i]['mensagem'] = '(Publicacao sem texto)'
            html += '<tr><td colspan="1">' + dados[i]['autor'] + '</td><td>' + dados[i]['mensagem'] + '</td><td><a href="%s' % dados[i]['link'] + '">Link</a></td><td><a href='"../comments?id=" + dados[i]['id'] + '' + ' role="button" class="btn btn-sm btn-success">Analizar</a></td></tr>'
            j += 1
        if j == QUANTIDADE_PUBLICACOES_PAGINA:
            break        
    html += ' <tbody id="tbody_conteudo"> </tbody> </table> </div> </div> '                        
    html += get_html_paginacao(len(dados), QUANTIDADE_PUBLICACOES_PAGINA, 'posts')
    return render(request, 'base.html', {'name': user_info.get('sobrenome'), 'conteudo_dinamico': html})

def get_html_paginacao(tamanho, quantidade_comentarios=5, redirect_page = 'posts', id_post = ''):
    html = '<ul id="paginacao" class="pagination pagination-lg">'
    
    limite = int(math.ceil(float(tamanho) / quantidade_comentarios)) 
    for i in xrange(0, limite):
        if id_post == 0:
            html += '<li id="%i' % int(i + 1) + '"><a href="../%s' % str(redirect_page) + '?page=%i' %int(i + 1) + '">%i' % int(i + 1) + '</a></li>'
        else:
            html += '<li id="%i' % int(i + 1) + '"><a href="../%s' % str(redirect_page) + '?page=%i' %int(i + 1) + '&id=%s">%i' % (id_post, int(i) + 1) + '</a></li>'
    html += '</ul>'
    return html    

def show_home(request):
    html = '<div class="jumbotron"> <h1>Seja bem-vindo ao Guessb!</h1><p>Este webapp faz análise de sentimentos (positivo, negativo ou neutro) em comentários escrito em português do Brasil, compartilhados por seguidores timeline do usuário dessa ferramenta. O classificador utilizado é o Multinomial Naive Bayes.</p></div></div>'
    return render(request, 'base.html', {'conteudo_dinamico':html})


def get_comentarios(request):
    numero_pagina = request.GET.get('page')
    
    if  numero_pagina == None:
        numero_pagina = 1
    
    html = '<div class="container theme-showcase" role="main"> <div class="row"> <div class="bs-example" data-example-id="panel-without-body-with-table"> <div class="panel panel-default"> <div class="panel-heading"><div class="btn-group pull-right">    <ul>    <li><input type="checkbox" value="pos" onclick="filtrar(this);" >Positivo</li>  <li><input type="checkbox" value="neg" onclick="filtrar(this);">Negativo</li>  <li><input type="checkbox" value="neu" onclick="filtrar(this);">Neutro</li></ul>    </div>   <h4>Publicacoes no Facebook</h4></div><table class="table table-stripped"> <thead>  <tr> <th colspan="1"> Usuario </th> <th> Post</th> <th> Acao </th> </tr> </thead> <tbody id="tbody_conteudo">'
    comentarios = get_coments(ACCESS_TOKEN, request.GET.get('id'))
    
    ultimo_indice = (QUANTIDADE_PUBLICACOES_PAGINA * int(numero_pagina)) 
    primeiro_indice = ultimo_indice - QUANTIDADE_PUBLICACOES_PAGINA
    
    j = 0
    
    for i in xrange(0, len(comentarios)):
        if i >= primeiro_indice and i < ultimo_indice:
            html += '<tr><td colspan="1">' + comentarios[i]['autor_comentario'] + '</td><td>' + comentarios[i]['comentario'] + '</td>' + '<td>' + comentarios[i]['polaridade'] + '</td></tr>'
            j += 1
        if j == QUANTIDADE_PUBLICACOES_PAGINA:
            break        
    html += ' <tbody id="tbody_conteudo"> </tbody> </table> </div> </div> '                        
    html += get_html_paginacao(len(comentarios), QUANTIDADE_PUBLICACOES_PAGINA, 'comments', request.GET.get('id'))
    return render(request, 'base.html', {'name': user_info.get('sobrenome'), 'conteudo_dinamico': html})

