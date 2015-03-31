from open_facebook.api import OpenFacebook

ACCESS_TOKEN = 'CAACEdEose0cBAC4enCapHZBsFwWJRgzLDmhBwsZAOPAsOqs6lvSUPJpEFT9MV9uMqwEZANRdNQz5MVeMTxhc2ZCucUsWFOCxQhNVaESYZBr7af4V2YSpttTTtYsnQXGCg56cx5ZARSJUt1lfNgZA8dslZApKibh1DSLViIikZCf2wNzBmEBCBiGvXTYSP9mDrX2c7toZClRqiAtI6yXpu1RpyO'
facebook_object = OpenFacebook(ACCESS_TOKEN)

def get_feed(token):
    facebook_object = OpenFacebook(ACCESS_TOKEN)
    feed_data = facebook_object.get('me/feed')
    array_conteudo = []
        
    for data in feed_data['data']:
        novos_comentarios = [] 
        link, mensagem, autor = '','',''
        
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
            array_conteudo.append(dict(autor=autor, mensagem=mensagem, link=link, comentarios=novos_comentarios))
        
        novos_comentarios = []
    return array_conteudo

for i in get_feed(ACCESS_TOKEN):
    print i



