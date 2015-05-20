from abc import abstractmethod, ABCMeta
from open_facebook.api import OpenFacebook
from tcc_appio.nltk_trainer_master.NBClassifierLoader import NBClassifierLoader

class DAOFactory(object):
    __metaclass__ = ABCMeta
    
    @staticmethod  
    def getDAOFactory():
        return FacebookDAOFactory()
    
    @abstractmethod
    def getGenericDAO(self):pass

class FacebookDAOFactory(DAOFactory):
    
    def getGenericDAO(self):
        return GenericDAOFacebook()    

class DAO:
    __metaclass__ = ABCMeta
    
    @abstractmethod
    def getFeed(self):pass
    
    @abstractmethod
    def getCommentsFeed(self, id):pass
    
class GenericDAOFacebook(DAO):
       
    def getCommentsFeed(self,ACCESS_TOKEN, id):
        facebookObject = OpenFacebook(ACCESS_TOKEN)
        feedData = facebookObject.get('me/feed')
        arrayComentarios = []
        novosComentarios = []
    
        for data in  feedData['data']:
            if data.get('id') == id:
                arrayComentarios = data.get('comments').get('data')
                
                for i in xrange(0, len(arrayComentarios)):
                    nbClassifier = NBClassifierLoader();
                    polaridade = self.getPolaridade(nbClassifier.classify(arrayComentarios[i].get('message','')))
                    
                    novosComentarios.append(
                                            dict(autor_id=arrayComentarios[i].get('from').get('id'),
                                                 autor_comentario=arrayComentarios[i].get('from').get('name'), 
                                                 comentario=arrayComentarios[i].get('message',''), polaridade=polaridade))
    
        return novosComentarios

    
    def getPolaridade(self, polaridade):
        if (polaridade == 'neu'):
            return 'Neutro'
    
        elif (polaridade == 'pos'):
            return "Positivo"
    
        return'Negativo'
    
    def getFeed(self, ACCESS_TOKEN):
        facebookObject = OpenFacebook(ACCESS_TOKEN)
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
