from abc import abstractmethod, ABCMeta
from open_facebook.api import OpenFacebook
from guessb.dao.NBClassifierLoader import NBClassifierLoader


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
    
    def __init__(self, accessToken):
        self._accessToken_ = accessToken        
    
    def getCommentsFeed(self, id, firstIndex, lastIndex):
        facebookObject = OpenFacebook(self._accessToken_)
        feedData = facebookObject.get('me/feed')
        content = []
        dictionaryComments = {'Positive' : 0, 'Negative' : 0, 'Neuter' : 0, 'All' : 0}
        classifier = NBClassifierLoader()
        
        for i in  xrange(0, len(feedData['data'])):
            if (feedData['data'][i].get('id') == id):
                comments = feedData['data'][i].get('comments').get('data')
                dictionaryComments['All'] = len(comments)
                
                for j in xrange(0, dictionaryComments['All']):
                    messageContent = comments[j].get('message', '')
                    authorName = comments[j].get('from').get('name')
                    authorId = comments[j].get('from').get('id')
                    polarity = self.getPolarity(classifier.classify(messageContent))
                    
                    self.countComments(dictionaryComments, polarity)
                    
                    content.append(dict(
                                    authorId=authorId,
                                    authorName=authorName,
                                    messageContent=messageContent,
                                    polarity=polarity))
                break
        return content, dictionaryComments
    
    def countComments(self, dictionaryComments, polarity):
        dictionaryComments[polarity] = int(dictionaryComments[polarity]) + 1 
    
    def getPolarity(self, polaridade):
        if (polaridade == 'neu'):
            return 'Neuter'
    
        elif (polaridade == 'pos'):
            return "Positive"
    
        return'Negative'
    
    def getFeed(self, firstIndex, lastIndex):
        facebookObject = OpenFacebook(self._accessToken_)
        feedData = facebookObject.get('me/feed')
        content = []
        profileName = facebookObject.get('me').get('name')
        profileId = facebookObject.get('me').get('id')
        
        for data in feedData['data']:
            if 'comments' in data:
                content.append(
                               dict(quantityComments=len(data.get('comments').get('data')),
                                    profileName=profileName,
                                    profileId=profileId,
                                    authorId=data.get('from').get('id'),
                                    authorName=data.get('from').get('name', ''),
                                    messageContent=data.get('message',
                                                            '(Post without text)'),
                                    link=data.get('link', '#'),
                                    postId=data.get('id')))
        
        self.getFeedPage(content)         
        return content
    

    def getFeedPage(self, content):
        facebookObject = OpenFacebook(self._accessToken_)
        accountData = facebookObject.get('me/accounts')
        pages = accountData.get('data')
        
        for page in pages:
            pageAccessToken = page.get('access_token')
            facebookObject = OpenFacebook(pageAccessToken)
            feedData = facebookObject.get('me/feed')
            profile = facebookObject.get('me')        
            
            for data in feedData['data']:
                if 'comments' in data:
                    content.append(dict(quantityComments=len(data.get('comments')),
                                        profileName=profile.get('name'),
                                        profileId=profile.get('id'),
                                        authorId=data.get('from').get('id'),
                                        authorName=data.get('from').get('name', ''),
                                        messageContent=data.get('message',
                                                                '(Post withouth text)'),
                                        link=data.get('link', '#'),
                                        postId=data.get('id'),
                                        accessToken=pageAccessToken))                                