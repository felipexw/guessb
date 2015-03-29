from open_facebook.api import OpenFacebook


ACCESS_TOKEN = "CAACEdEose0cBAAdyq7EIUZBNZAyJA902b7pJZBZARpmewwIKI9gysZC5hC5EcWgyVJWoqZBYciiiGpH5eVVIMIZB5reWgmaFZCWA6zNCgaZAsTgtvVEinGLv9jewbjPzZA8JIKFTDVWuKZAaLjKnLlstCwV4V9AUJsI4mSNXNSGT6ZADMKqZC1ZAqkQzgO8v3v9TSTIpdYaSqLuJeSixnbFFb2Y8wx"
facebook = OpenFacebook(ACCESS_TOKEN)
def get_photos(facebook_object):
    videos = facebook_object.get('me/feed')
    for i in videos['data']:
        descricao_foto = i.get('name', 'none')
        array_comentarios = i.get('comments', 'null')
        print 'Descricao: ' + descricao_foto
        if array_comentarios != 'null':
           print '---comentariosss---'
           array_data = array_comentarios['data']
           for j in xrange(0, len(array_data)):
            print 'autor do comentario: ' + array_data[j]['from']['name']
            print 'comentario: ' + array_data[j]['message']                
def get_links(facebook_object):
    data = facebook_object.get('me/links')
    for post in data['data']:
        print '\nautor: ' + post.get('from', 'none').get('name', 'none')
        print 'nome: '  + post.get('name', 'none')
        print 'link: ' + post.get('link', 'none')
        print 'mensagem: ' + post.get('message', 'none')
        print 'description: ' + post.get('description', 'none')
        comments = post.get('comments', 'none')

        if comments != 'none':
           array_comments = comments.get('data', 'none')
           print '\n---comentarios---'
        
        for i in xrange(0, len(array_comments)):
            autor_comentario = array_comments[i].get('from','none').get('name', 'none')
            mensagem_comentario = array_comments[i].get('message', 'none')
            print 'autor: ' + autor_comentario
            print 'comentario: ' + mensagem_comentario                
        
get_links(facebook)