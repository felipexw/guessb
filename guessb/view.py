# coding= utf-8
'''Created on 20/03/2015

@author: felipexw
'''
from django.shortcuts import render
from guessb.dao.DAO import *
import math
from django.http.response import HttpResponse

def showAnotherHome(request):
    print 'def showAnotherHome(request):'
    html = ''
    if 'ACCESS_TOKEN' in request.session:
        html = '<div id="jumbotron" class="jumbotron"> <h1>Welcome to Guessb!</h1><p>The Guessb webapp its the Bachelors Thesis presented to the University of the State of Santa Catarina, as a requirement to the bachelor degree.</p></div></div>'
    
    else:
        html = '<div class="content">    <div class="form-group">   <label for="exampleInputPassword1">Token</label><input type="text" class="form-control" id="accessTokenInput"> </div><button type="submit" class="btn btn-default" onclick="showAnotherHome()">Submit</button>  </div>'
    
    return render(request, 'base_2.html', {'conteudo_dinamico':html})

def showAbout(request):
    html = '<div id="jumbotron" class="jumbotron"> <h1>Welcome to Guessb!</h1><p>The Guessb webapp its the Bachelors Thesis presented to the University of the State of Santa Catarina, as a requirement to the bachelor degree.</p></div></div>'
    return HttpResponse(html)

def getPaginationIndexes(pageNumber, numberPostsPage):
    print 'def getPaginationIndexes('
    try:
        if numberPostsPage == None:
            numberPostsPage = 10
    
        if  pageNumber == None:
            pageNumber = 1
    
        lastIndex = math.fabs((int(numberPostsPage) * int(pageNumber)))
        firstIndex = math.fabs(int(lastIndex) - int(numberPostsPage))
    except Exception as e:
        print e
    return firstIndex, lastIndex, numberPostsPage

def __checkCookie(request):
    if not 'ACCESS_TOKEN' in request.session._session:
        request.session['ACCESS_TOKEN'] = request.GET.get('ACCESS_TOKEN')
        request.session.set_expiry(3600)    

def __checkAccessTokenPostId(content, request):
    for data in content:
        if 'accessToken' in data:
            if  data.get('postId') not in request.session:
                request.session[data.get('postId')] = data.get('accessToken')
           
def showPosts(request):
    firstIndex, lastIndex, numberPostsPage = getPaginationIndexes(request.GET.get('page'), request.GET.get('totalNumberPosts'))
    html = ''
    response = HttpResponse()
    
    __checkCookie(request)
    
    content = []
    try:
        factory = DAOFactory.getDAOFactory()	
        content = factory.getGenericDAO(request.session.get('ACCESS_TOKEN')).getFeed(firstIndex, lastIndex)
        html += '<div class="container theme-showcase" role="main"> <div class="row">  <div class="bs-example" data-example-id="panel-without-body-with-table"> <div class="panel panel-default"><div class="panel-heading"><h4>Posts on Facebook</h4></div><table class="table table-hover"> <thead>  <tr><th> Profile </th> <th> Author </th> <th> Post</th><th>N. Comments</th> <th> Link </th> <th> Action </th> </tr> </thead> <tbody id="tbody_conteudo">'
        
        __checkAccessTokenPostId(content, request)
    except Exception as e:
        html = '<div id="jumbotron" class="jumbotron"> <p>Your session has expired. Please connect again.</p></div>'
        try:
            request.session.__delitem__('ACCESS_TOKEN')
        except Exception as ec:
            print ec
	
    else:
        j = 0
        
        for i in xrange(0, len(content)):
            if i >= firstIndex and i < lastIndex:
                profileImg = '<img  src="//graph.facebook.com/' + content[i].get('profileId') + '/picture?type=large"' + ' style="width: 45px; height: 45px;" class="img-circle"/>' 
                img = '<img  src="//graph.facebook.com/' + content[i].get('authorId') + '/picture?type=large"' + ' style="width: 75px; height: 75px;" class="img-circle"/>'
                postId = "'%s'" % content[i]['postId']
                st = "showCommentsFromPosts(%s,%s)" % ('1', postId)
                try:
                    html += '<tr><td>' + profileImg + '<p style="text-align: center">' + content[i]['profileName'] + '</p>  </td><td>' + img + '<p style="text-align: center">' + content[i]['authorName'] + '</p>  </td><td><p>' + content[i]['messageContent'] + '</p></td><td><p>%i' % content[i]['quantityComments']+'</p><td><p><a href="%s' % content[i]['link'] + '">Link</a></p></td><td><p><button type="button" onclick=%s' % st + ' role="button" class="btn btn-md btn-success"><i class="glyphicon glyphicon-tag icon-th"></i></a></p></td></tr>'
                except Exception as e:
                    print e
                j += 1
                if j == numberPostsPage:
                    break        
    
        html += ' <tbody id="tbody_conteudo"> </tbody> </table> </div> </div> '                        
        html += __get_html_paginacao(len(content), numberPostsPage, "'posts'", '', request.GET.get('page'))

    response.write(html)
    return response    

def __get_html_paginacao(tamanho, commentsNumber=5, redirect_page="'posts'", postId='', page='0'):
    html = '<ul id="paginacao" class="pagination pagination-lg">'
    
    limite = int(math.ceil(float(tamanho) / float(commentsNumber))) 
    functionName = ''
    
    for i in xrange(0, limite):
        className = ''
        if page == str(i + 1):
            className = 'active' 
        
        if redirect_page == "'posts'":
            functionName = 'showPosts(%s, %i)' % ('1', int(i + 1))
        
        else:
            functionName = "showCommentsFromPosts(%i, '%s')" % (int(i + 1), postId) 
        
        if postId == 0:
            html += '<li class=%s' % className + '" id="%i' % int(i + 1) + '"><a onclick="%s" ' % functionName + 'href="javascript:void(0)">%i' % int(i + 1) + '</a></li>'
        else:
            html += '<li class="%s' % className + '" id="%i' % int(i + 1) + '"><a onclick="%s" ' % functionName + 'href="javascript:void(0)">%i' % (int(i) + 1) + '</a></li>'
    html += '</ul>' 
    return html    

def showHome(request):
    html = '<div id="jumbotron" class="jumbotron"> <h1>Welcome to Guessb!</h1><p>The Guessb webapp do sentiment analysis (positive, negative or neuter) in Brazil portuguese comments, shared by another users on a give users timeline. The machine learning techinique used in the Guessb webapp is the Multinomial Naive Bayes.</p></div></div>'
    return render(request, 'base.html', {'conteudo_dinamico':html})

def __getAccessTokenPostIt(request, postId):
    if postId in request.session:
        return request.session.get(postId)
    
    return request.session.get('ACCESS_TOKEN')

def __getHtmlPanelHeadComments(dictionaryComments):
    html = '<div class="panel panel-default"><div class="panel-heading">  <div class="pull-right">  <div id="div_btn_group" onclick="updateStatusButtonGroup(this)" class="btn-group" class="btn-group"><button type="button" class="multiselect dropdown-toggle btn btn-default" data-toggle="dropdown" title=""><i class="glyphicon glyphicon-th icon-th"></i> <b class="caret"></b></button><ul class="multiselect-container dropdown-menu"><li>  <a tabindex="0">    <label class="checkbox">      <input onclick="filter();" type="checkbox" checked="true" value="Positive" name="check_box">Positive</label> </a></li> <li><a tabindex="0"> <label class="checkbox"> <input type="checkbox" onclick="filter();" value="Negative" name="check_box" checked="">Negative </label></a></li><li><a tabindex="0"><label class="checkbox"> <input type="checkbox" onclick="filter();" value="Neuter" name="check_box" checked="">Neuter</label></a></li></ul></div></div><h3>Sentiment Analysis of Posts on Facebook</h3><div class="progress">'
    positivePercent =  round(float(dictionaryComments.get('Positive')) / float(dictionaryComments.get('All')), 2) * 100
    negativePercent =  round(float(dictionaryComments.get('Negative')) / float(dictionaryComments.get('All')), 2) * 100
    neuterPercent = round(float(dictionaryComments.get('Neuter')) / float(dictionaryComments.get('All')), 2) * 100
    
    if positivePercent > 0:
        html += '<div class="progress-bar progress-bar-success progress-bar-striped" style="width:' + str(positivePercent) + '%"><p>' + str(positivePercent) + '% Positive</p> </div>'
    
    if negativePercent > 0:
        html += '<div class="progress-bar progress-bar-danger progress-bar-striped" style="width: ' + str(negativePercent) + '%"><p>' + str(negativePercent) + '% Negative</p></div>'
    
    if neuterPercent > 0:
        html += '<div class="progress-bar progress-bar-info progress-bar-striped" style="width: ' + str(neuterPercent) + '%"> <p>' + str(neuterPercent) + '% Neuter </p> </div>'

    html += '</div></div><table class="table table-hover"> <thead>  <tr> <th> Author </th> <th> Post</th> <th> Label     </th> </tr> </thead> <tbody id="tbody_conteudo">'
    return html

def showComments(request):
    html = '' 
    try:
        firstIndex, lastIndex, numberPostsPage = getPaginationIndexes(request.GET.get('page'), request.GET.get('totalNumberPosts'))

        response = HttpResponse()
    
        __checkCookie(request)
        content = []
    
        factory = DAOFactory.getDAOFactory()
        accessToken = __getAccessTokenPostIt(request, request.GET.get('postId'))
        content, dictionaryComments = factory.getGenericDAO(accessToken).getCommentsFeed(request.GET.get('postId'), firstIndex, lastIndex)
    except Exception as e:
        html = '<div id="jumbotron" class="jumbotron"> <p>Your session has expirde. Please conect again.</p></div>'
        print e
    else:
        html = __getHtmlPanelHeadComments(dictionaryComments)
        j = 0
        
        for i in xrange(0, len(content)):
            if i >= firstIndex and i < lastIndex:
                html += '<tr><td> <img  src="//graph.facebook.com/' + content[i]['authorId'] + '/picture?type=large" style="width: 75px; height: 75px;" class="img-circle "/><p style="text-align: center">' + content[i]['authorName'] + '</p></td><td>' + content[i]['messageContent'] + '</td>' + '<td>' + content[i]['polarity'] + '</td></tr>'
                j += 1
            if j ==  numberPostsPage:
                break
        html += '</tbody> </table> </div> </div> '                        
        html += __get_html_paginacao(dictionaryComments['All'], numberPostsPage, "'comments'", request.GET.get('postId'), request.GET.get('page'))
    
    response.write(html)
    return response

def __getHtmlNumberPage_(length):
    html = '<div class="btn-group" onclick="updateStatusButtonGroup(this)"> <button type="button" class="btn btn-default dropdown-toggle" data-toggle="dropdown" aria-expanded="false">Publicacoes/pagina <span class="caret"></span> </button> <ul class="dropdown-menu" role="menu">'
    limit = math.ceil(float(length) / float(10))
    
    for i in xrange(1, int(limit)):
        html += '<li><a href="javascript:void(0)" onclick="showPostsPerNumber(1, 1, ' + str((i * 10)) + ')" >' + str(i * 10) + '</a></li>'
    
    html += '<li><a href="javascript:void(0)" onclick="showPostsPerNumber(1, 1,' + str(length) + '>Todos</a></ul></div>'
    return html
