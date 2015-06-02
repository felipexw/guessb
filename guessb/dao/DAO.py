from abc import abstractmethod, ABCMeta
from open_facebook.api import OpenFacebook
from guessb.nltk_trainer_master.NBClassifierLoader import NBClassifierLoader
from oauthlib.oauth1.rfc5849.endpoints import access_token

class DAOFactory(object):
    __metaclass__ = ABCMeta
    
    @staticmethod  
    def getDAOFactory():
        return FacebookDAOFactory()
    
    @abstractmethod
    def getGenericDAO(self, ACCESS_TOKEN):pass

class FacebookDAOFactory(DAOFactory):
    
    def getGenericDAO(self, ACCESS_TOKEN):
        return GenericDAOFacebook(ACCESS_TOKEN)    

class DAO:
    __metaclass__ = ABCMeta
    
    @abstractmethod
    def getFeed(self):pass
    
    @abstractmethod
    def getCommentsFeed(self, id):pass
    
class GenericDAOFacebook(DAO):
    
    def __init__(self, ACCESS_TOKEN):
        self.ACCESS_TOKEN = ACCESS_TOKEN
        print self.ACCESS_TOKEN 
    
    def getCommentsFeed(self, id):
        facebookObject = OpenFacebook(self.ACCESS_TOKEN)
        feedData = facebookObject.get('me/feed')
        comments = []
        content = []
    
        for data in  feedData['data']:
            if data.get('id') == id:
                comments = data.get('comments').get('data')
                
                for i in xrange(0, len(comments)):
                    classifier = NBClassifierLoader();
                
                    messageContent = comments[i].get('message', '')
                    authorName = comments[i].get('from').get('name')
                    authorId = comments[i].get('from').get('id')
                    polarity = classifier.classify(messageContent)
                    
                    content.append(dict(authorId=authorId,
                                                 authorName=authorName,
                                                  messageContent=messageContent,
                                                   polarity=self.getPolaridade(polarity)))
        return content

    
    def getPolaridade(self, polaridade):
        if (polaridade == 'neu'):
            return 'Neutro'
    
        elif (polaridade == 'pos'):
            return "Positivo"
    
        return'Negativo'
    
    def getFeed(self):
        facebookObject = OpenFacebook(self.ACCESS_TOKEN)
        feedData = facebookObject.get('me/feed')
        content = []
        
        for data in feedData['data']:
            if not 'comments' in data:
                continue
            else:
                content.append(
                               dict(authorId=data.get('from').get('id'),
                                    authorName=data.get('from').get('name', ''),
                                    messageContent=data.get('message',
                                                       '(Postagem sem texto)'),
                                    link=data.get('link'),
                                    postId=data.get('id')))
        
        return content
