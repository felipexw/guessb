#coding: utf-8
from open_facebook.api import OpenFacebook
from naive_bayes_classifier import classify
ACCESS_TOKEN = "CAACEdEose0cBAFME1XiibWVSrD7TKdqCXONzLLamZAi8p4ex8IcbGpbAIh1ibxvIwbGPfkuJTpJLc5wtcH89T27ZB5sXoKH19febdoZBc8SQLOjRWXY4cij11IH4UogxGnCrICMqB8MSYW3JFEQQRlTEybS9P3Ww3BbACcVoqwGVeTFts2l6J3HLHCT1tcmNDQjyZBkmSWFEH6ZAQTur9"
def get_feed(token):
    facebook_object = OpenFacebook(token)
    feed_data = facebook_object.get('me/feed')
    array_conteudo = []
        
    for data in feed_data['data']:
        novos_comentarios = [] 
        link, mensagem, autor = '','',''
        print data['id']
        if 'comments' in data:
            array_comentarios = data.get('comments').get('data')
            
            for i in xrange(0, len(array_comentarios)):
                novos_comentarios.append(
                                         dict(autor_comentario=array_comentarios[i].get('from').get('name'),comentario=array_comentarios[i].get('message')))
            
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
                polaridade = classify(array_comentarios[i].get('message'))
                print polaridade
                novos_comentarios.append(
                                         dict(autor_comentario=array_comentarios[i].get('from').get('name'),comentario=array_comentarios[i].get('message'),polaridade=polaridade))
    
    return novos_comentarios

    

    