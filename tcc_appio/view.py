'''
Created on 20/03/2015

@author: felipexw
'''
from django.http.response import HttpResponse
from django.shortcuts import render

def login_home(request):
    name = 'Felipe Appio'
    return render(request, 'login_twitter.html', {'name': name})

def hello(requet):
    return HttpResponse("Hello world")

def test_template(request):
    name = 'Appio'
    return render(request, 'base.html', {'name': name})