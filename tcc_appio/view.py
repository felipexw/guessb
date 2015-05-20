# coding= utf-8
'''Created on 20/03/2015

@author: felipexw
'''
from django.shortcuts import render
from tcc_appio.dao.DAO import DAO, DAOFactory, FacebookDAOFactory, GenericDAOFacebook

import math

ACCESS_TOKEN = 'CAACEdEose0cBABH3PvI4jW21UsSC4wnINzJB9ZBB6MErYRIv9K0ZB8ER6kd6xZBTxMNtWHoN3aIe1DiTaBGhaq8ZB6fkfnXFeyxPx1nvSPQRxZAXkdmtibjcKhH36NrJeTNsZClZBY5VU6ce3MJUVDtBgYS437KFYwGvhetUZCrC8slHf71ejAkNTGnv32QVzvKvjVwReALoLhsgqd6FJWwd    '
QUANTIDADE_PUBLICACOES_PAGINA = 5


def show_about(request):
    html = '<div class="jumbotron"> <h1>Seja bem-vindo ao Guessb!</h1><p>Este webapp é o Trabalho de Conclusão apresentado ao Curso de Sistemas de Informação, da Universidade do Estado de Santa Catarina, como requisito parcial para obtenção do grau de Bacharel em Sistemas de Informação.</p></div></div>'
    return render(request, 'base.html', {'conteudo_dinamico':html})

def get_indices_paginacao(numero_pagina):
    if  numero_pagina == None:
        numero_pagina = 1
    
    ultimo_indice = (QUANTIDADE_PUBLICACOES_PAGINA * int(numero_pagina))
    primeiro_indice = ultimo_indice - QUANTIDADE_PUBLICACOES_PAGINA
    return primeiro_indice, ultimo_indice
     
def show_posts(request):
    primeiro_indice, ultimo_indice = get_indices_paginacao(request.GET.get('page'))
    html = '<div class="container theme-showcase" role="main"> <div class="row">  <div class="bs-example" data-example-id="panel-without-body-with-table"> <div class="panel panel-default"><div class="panel-heading"><h4>Publicacoes no Facebook</h4></div><table class="table table-stripped"> <thead>  <tr> <th colspan="1"> Usuario </th> <th> Post</th> <th> Link </th> <th> Acao </th> </tr> </thead> <tbody id="tbody_conteudo">'
        
    factory = DAOFactory.getDAOFactory()
    dados = factory.getGenericDAO().getFeed(ACCESS_TOKEN)
    
    j = 0
    
    for i in xrange(0, len(dados)):
        if i >= primeiro_indice and i < ultimo_indice:
            img = '<img  src="//graph.facebook.com/'+dados[i].get('autor_id')+'/picture?type=large"' + ' style="width: 75px; height: 75px;" class="img-circle"/>'
            html += '<tr><td>'+img+'<p style="text-align: center">'+ dados[i]['autor'] + '</p>  </td><td>' + dados[i]['mensagem'] + '</td><td><a href="%s' % dados[i]['link'] + '">Link</a></td><td><a href='"../comments?id=" + dados[i]['id'] + '' + ' role="button" class="btn btn-sm btn-success">Analizar</a></td></tr>'
            j += 1
        if j == QUANTIDADE_PUBLICACOES_PAGINA:
            break        
    html += ' <tbody id="tbody_conteudo"> </tbody> </table> </div> </div> '                        
    html += get_html_paginacao(len(dados), QUANTIDADE_PUBLICACOES_PAGINA, 'posts')
    return render(request, 'base.html', {'conteudo_dinamico': html})

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
    primeiro_indice, ultimo_indice = get_indices_paginacao(request.GET.get('page'))
    
    html = '<div class="container theme-showcase" role="main"> <div class="row"> <div class="bs-example" data-example-id="panel-without-body-with-table"> <div class="panel panel-default"> <div class="panel-heading">  <div class="pull-right">  <div id="div_btn_group" onclick="showFilters(this)";class="btn-group"><button type="button" class="multiselect dropdown-toggle btn btn-default" data-toggle="dropdown" title=""><i class="glyphicon glyphicon-th icon-th"></i> <b class="caret"></b></button><ul class="multiselect-container dropdown-menu"><li>  <a tabindex="0">    <label class="checkbox">      <input onclick="filter();"type="checkbox" checked="true" value="Positivo" name="check_box" checked>Positivo</label> </a></li> <li><a tabindex="0"> <label class="checkbox"> <input type="checkbox" onclick="filter();" value="Negativo" name="check_box" checked>Negativo </label></a></li><li><a tabindex="0"><label class="checkbox"> <input type="checkbox"  onclick="filter();" value="Neutro" name="check_box" checked>Neutro</label></a></li></ul></div></div><h4>Publicacoes no Facebook</h4></div><table class="table table-stripped"> <thead>  <tr> <th> Usuario </th> <th> Post</th> <th> Classificacao     </th> </tr> </thead> <tbody id="tbody_conteudo">'
    
    comentarios = DAOFactory.getDAOFactory().getGenericDAO().getCommentsFeed(ACCESS_TOKEN, request.GET.get('id'))
    
    j = 0
    
    for i in xrange(0, len(comentarios)):
        if i >= primeiro_indice and i < ultimo_indice:
            html += '<tr><td> <img  src="//graph.facebook.com/'+ comentarios[i]['autor_id']+'/picture?type=large" style="width: 75px; height: 75px;" class="img-circle "/><p style="text-align: center">' + comentarios[i]['autor_comentario'] + '</p></td><td>' + comentarios[i]['comentario'] + '</td>' + '<td>' + comentarios[i]['polaridade'] + '</td></tr>'
            j += 1
        if j == QUANTIDADE_PUBLICACOES_PAGINA:
            break        
    html += '</tbody> </table> </div> </div> '                        
    html += get_html_paginacao(len(comentarios), QUANTIDADE_PUBLICACOES_PAGINA, 'comments', request.GET.get('id'))
    return render(request, 'base.html', {'conteudo_dinamico': html})

