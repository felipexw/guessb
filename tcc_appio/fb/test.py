from open_facebook.api import OpenFacebook



ACCESS_TOKEN = "CAACEdEose0cBAA5eyt9vzx9WfhsYcZBs6EZATxEd3PfTDD7FZAvnQgMZAcUrZBqi5PKbOlyOp3rP3NOQ2zkGidnodksZAbCYSilLZCWNMk4q7cbwtZCXZCLLKd8lDHDUyPoaH5Jt7nbgSukijW7fptyidVZAvp00whGHAMA9yLQGIVhVmBMIiC9xZAZCdofKjRhDyZBPU8P6kcIwNVmXgflGnKgaC"
facebook = OpenFacebook(ACCESS_TOKEN)

def contains_key(structure, key):
    return key in structure

def get_feed(facebook_object):
    feed_data = facebook_object.get('me/feed')
    
    dicionario_conteudo = {}
    for data in feed_data['data']:
        for j in xrange(0, len(data)):
            
            str_resultado = ''
            if 'name' in data.keys():
                str_resultado += 'name: ' + data['name'] 
            if 'message' in data.keys():
                str_resultado += ' \nmessage: ' + data['message']
            if 'link' in data.keys():
                str_resultado += ' link: ' + data['link'] 
        
            
            str_resultado += ' type: ' + data['type'] 

            #if 'comments' in data['comments']:
                #comentarios = data['comments']['data']
                #str_resultado += '\n---comentarios--- '
                #for k in xrange(0, len(comentarios)):
                    #str_resultado += ' autor do comentario: ' + comentarios[k]['from']['name'] 
                    #str_resultado += '\ncomentario: ' + comentarios['message']
                    
        print str_resultado                        



def get_links(facebook_object):
    data = facebook_object.get('me/links')
    for post in data['data']:
        print '\nautor: ' + post.get('from', 'none').get('name', 'none')
        print 'nome: ' + post.get('name', 'none')
        print 'link: ' + post.get('link', 'none')
        print 'mensagem: ' + post.get('message', 'none')
        print 'description: ' + post.get('description', 'none')
        comments = post.get('comments', 'none')


        if comments != 'none':
           array_comments = comments.get('data', 'none')
           print '\n---comentarios---'
        
        for i in xrange(0, len(array_comments)):
            autor_comentario = array_comments[i].get('from', 'none').get('name', 'none')
            mensagem_comentario = array_comments[i].get('message', 'none')
            print 'autor: ' + autor_comentario
            print 'comentario: ' + mensagem_comentario                

get_feed(facebook)







