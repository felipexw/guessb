from open_facebook.api import OpenFacebook
from naive_bayes_classifier import classify
from UserString import MutableString

class MainController(object):
    def getPolaridade(self, polaridade):
        if (polaridade == 'neu'):
            return 'Neutro'
    
        elif (polaridade == 'pos'):
            return "Positivo"
    
        return'Negativo'

    
    def getFeed(self,token):
        facebookObject = OpenFacebook(token)
        feedData = facebookObject.get('me/feed')
        arrayConteudo = []
        
        for data in feedData['data']:
            if not 'comments' in data:
                continue
            else:
                arrayConteudo.append(
                                     dict(autor_id=data.get('from').get('id'), autor=data.get('from').get('name',''), 
                                          mensagem=data.get('message','(Postagem sem texto)'), link=data.get('link'), id=data.get('id')))
        
        return arrayConteudo

    def getComments(self,token, id):
        facebookObject = OpenFacebook(token)
        feedData = facebookObject.get('me/feed')
        arrayComentarios = []
        novosComentarios = []
    
        for data in  feedData['data']:
            if data.get('id') == id:
                arrayComentarios = data.get('comments').get('data')
                
                for i in xrange(0, len(arrayComentarios)):
                    polaridade = self.getPolaridade(classify(arrayComentarios[i].get('message','')))
                    
                    novosComentarios.append(
                                            dict(autor_id=arrayComentarios[i].get('from').get('id'),autor_comentario=arrayComentarios[i].get('from').get('name'), comentario=arrayComentarios[i].get('message',''), polaridade=polaridade))
    
        return novosComentarios

