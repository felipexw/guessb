# coding=utf-8
'''Created on 20/03/2015

@author: felipexw
'''
from django.http.response import HttpResponse
from django.shortcuts import render
from main_controller import get_feed
ACCESS_TOKEN = 'CAACEdEose0cBAC4enCapHZBsFwWJRgzLDmhBwsZAOPAsOqs6lvSUPJpEFT9MV9uMqwEZANRdNQz5MVeMTxhc2ZCucUsWFOCxQhNVaESYZBr7af4V2YSpttTTtYsnQXGCg56cx5ZARSJUt1lfNgZA8dslZApKibh1DSLViIikZCf2wNzBmEBCBiGvXTYSP9mDrX2c7toZClRqiAtI6yXpu1RpyO'
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
        html += '<tr><td colspan="1">'+conteudo['autor']+'</td><td>'+conteudo['mensagem']+'</td><td><button type="button" class="btn btn-sm btn-success">Verificar</button></td></tr>'

    html += '</tbody></table></div>'                        
    return render(request, 'base.html', {'name': name, 'conteudo': html})

