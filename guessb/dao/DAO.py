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
    def getFeed(self, firstIndex, lastIndex):pass
    
    @abstractmethod
    def getCommentsFeed(self, id, firstIndex, lastIndex):pass
    
class GenericDAOFacebook(DAO):
    
    def __init__(self, ACCESS_TOKEN):
        self.ACCESS_TOKEN = ACCESS_TOKEN
        print self.ACCESS_TOKEN 
    
    def getCommentsFeed(self, id, firstIndex, lastIndex):
        facebookObject = OpenFacebook(self.ACCESS_TOKEN)
        feedData = facebookObject.get('me/feed')
        comments = []
        content = []
        
        commentsLength = 0
        
        classifier = NBClassifierLoader();
        finished = False
        
        for i in  xrange(0, len(feedData['data'])):
            if finished:
                break
           
            if (feedData['data'][i].get('id') == id):
                finished = True
                
                comments = feedData['data'][i].get('comments').get('data')
                commentsLength = len(comments)
               
                for j in xrange(0, commentsLength):
                    if (j >= firstIndex) and (j < lastIndex):
                        messageContent = comments[j].get('message', '')
                        authorName = comments[j].get('from').get('name')
                        authorId = comments[j].get('from').get('id')
                        polarity = classifier.classify(messageContent)
                    
                        content.append(dict(authorId=authorId,
                                                            authorName=authorName,
                                                            messageContent=messageContent,
                                                            polarity=self.getPolaridade(polarity)))
                        
        return content, commentsLength

    
    def getPolaridade(self, polaridade):
        if (polaridade == 'neu'):
            return 'Neutro'
    
        elif (polaridade == 'pos'):
            return "Positivo"
    
        return'Negativo'
    
    def getFeed(self, firstIndex, lastIndex):
        facebookObject = OpenFacebook(self.ACCESS_TOKEN)
        feedData = facebookObject.get('me/feed')
        content = []
        
        for data in feedData['data']:
            if 'comments' in data:
                content.append(
                               dict(authorId=data.get('from').get('id'),
                                    authorName=data.get('from').get('name', ''),
                                    messageContent=data.get('message',
                                                                      '(Postagem sem texto)'),
                                    link=data.get('link'),
                                    postId=data.get('id')))
                 
        return content
