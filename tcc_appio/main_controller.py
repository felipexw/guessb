# coding: utf-8
from open_facebook.api import OpenFacebook
from naive_bayes_classifier import classify

def get_feed(token):
    facebook_object = OpenFacebook(token)
    feed_data = facebook_object.get('me/feed')
    array_conteudo = []
        
    for data in feed_data['data']:
        print data
        novos_comentarios = [] 
        link, mensagem, autor = '', '', ''
        
        if 'comments' in data:
            array_comentarios = data.get('comments').get('data')
            
            for i in xrange(0, len(array_comentarios)):
                novos_comentarios.append(
                                         dict(autor_comentario=array_comentarios[i].get('from').get('name'), comentario=array_comentarios[i].get('message')))
            
        autor = data['from']['name'] 
        
        if 'message' in data:
            mensagem = data.get('message')
            
        if 'link' in data:
            link = data.get('link')
        
        if len(novos_comentarios) > 0:    
            array_conteudo.append(dict(autor=autor, mensagem=mensagem, link=link, comentarios=novos_comentarios, id=data['id']))
        
        novos_comentarios = []
    return array_conteudo

def get_coments(token, id):
    facebook_object = OpenFacebook(token)
    feed_data = facebook_object.get('me/feed')
    array_comentarios = []
    novos_comentarios = []
    
    for data in  feed_data['data']:
        if data.get('id') == id:
            array_comentarios = data.get('comments').get('data')
            
            for i in xrange(0, len(array_comentarios)):
                polaridade = get_polaridade(classify(array_comentarios[i].get('message')))                
                novos_comentarios.append(
                                         dict(autor_comentario=array_comentarios[i].get('from').get('name'), comentario=array_comentarios[i].get('message'), polaridade=polaridade))
    
    return novos_comentarios

def get_user_info(token):
    facebook_object = OpenFacebook(token)
    data = facebook_object.get('me')
    return {'sobrenome': data.get('last_name')}

def get_polaridade(polaridade):
    if (polaridade == 'neu'):
        return 'Neutro'        
    
    elif (polaridade == 'neg'):
        return 'Negativo'
    
    return "Positivo"
