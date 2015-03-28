from open_facebook.api import OpenFacebook


ACCESS_TOKEN = "CAACEdEose0cBAJzgZCd18E80ZC3DsdnU3drVWQbZCZBNKuQ44BO4gRig8ygIsI8uBpToy5LO9Q1RtzuLiKd5zwIZByVIMaZCpCTtmoZANnZBz5wzOlr2ZCkhg5iNQu1qVzDMdxMu5AEVE52a3Bl1DPziiOZAlZCHdSsh9ewMFgzGuYz2ju5Htk0Ep5d0BPZA4IoSE1zezB1TGq7xfZAHJZCZAgZAQYZB2"
facebook = OpenFacebook(ACCESS_TOKEN)

def get_statuses(facebook_object):
    arr_statuses = []
    statuses = facebook_object.get('me/statuses')
    for s in statuses['data']:
        arr_statuses.append(s['message'])

    return arr_statuses

def get_videos(facebook_object):
    videos = facebook_object.get('me/photos')
    
    for i in videos['data']:
        print i
        descricao_foto = i.get('name', 'none')
        array_comentarios = i.get('comments', 'null')
        print 'Descricao: ' + descricao_foto
        
        if array_comentarios != 'null':
            print '---comentariosss---'
            array_data = array_comentarios['data']
            for j in xrange(0, len(array_data)):
                print 'autor do comentario: ' + array_data[j]['from']['name']
                print 'comentario: ' + array_data[j]['message'] 
                # nome do Carinha que fez o comentario: print array_data[j]['from']['name']
                # comentario em si print array_data[j]['message']
            
get_videos(facebook)

