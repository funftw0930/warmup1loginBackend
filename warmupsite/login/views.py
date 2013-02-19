# Create your views here.
from django.http import HttpResponse
from models import Users
import json
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
import os

@csrf_exempt
def initpage(request):
    return render(request, 'client.html')

@csrf_exempt
def login(request):
    inp = json.loads(request.raw_post_data)
    return HttpResponse(json.dumps(loginHelp(inp)), content_type="application/json")

def loginHelp(inp):
    outp = {}
    try:
        u = Users.objects.get(name = inp['user'])
    except Users.DoesNotExist:
        outp['errCode'] = -1
    else:
        if u.password == inp['password']:
            u.logcount += 1
            u.save()
            outp['errCode'] = 1
            outp['count'] = u.logcount
        else:
            outp['errCode'] = -1
    return outp
    
@csrf_exempt
def add(request):
    inp = json.loads(request.raw_post_data)
    return HttpResponse(json.dumps(addHelp(inp)), content_type="application/json")

def addHelp(inp):
    outp = {}
    if len(inp['user']) > 128 or inp['user'] == '':
        outp['errCode'] = -3
    elif len(inp['password']) > 128:
        outp['errCode'] = -4
    else:    
        try:
            u = Users.objects.get(name = inp['user'])
        except Users.DoesNotExist:
            new_u = Users(name=inp['user'], password=inp['password'], logcount=1)
            new_u.save()
            outp['errCode'] = 1
            outp['count'] = 1
        else:
            outp['errCode'] = -2
    return outp


@csrf_exempt
def resetFixture(request):
    Users.objects.all().delete()
    return HttpResponse(json.dumps({'errCode':1}), content_type="application/json")

    

@csrf_exempt
def testUnit(request):
    fail = 10
    outp = {}
    outp['output'] = ''
    outp['totalTests'] = 10
    Users.objects.all().delete()
    #test adding users
    if addHelp({'user':'user1', 'password':'password'}) == {'errCode':1, 'count':1}:
        fail-=1
    else:
        outp['output'] += 'TEST_1 fail: user not added correctly; ' 
    if addHelp({'user':'user2', 'password':''}) == {'errCode':1, 'count':1}:
        fail-=1
    else:
        outp['output'] += 'TEST_2 fail: user not added correctly; '
    if addHelp({'user':'user1', 'password':'password'}) == {'errCode':-2}:
        fail-=1
    else:
        outp['output'] += 'TEST_3 fail: duplicate user not identified; '
    if addHelp({'user':'', 'password':'password'}) == {'errCode':-3}:
        fail-=1
    else:
        outp['output'] += 'TEST_4 fail: no-name user not rejected; '

    Users.objects.all().delete()
    if addHelp({'user':'user1', 'password':'password'}) == {'errCode':1, 'count':1}:
        fail-=1
    else:
        outp['output'] += 'TEST_5 fail: user table not wiped; '

    #test login
    if loginHelp({'user':'user1', 'password':'password'}) == {'errCode':1, 'count':2}:
        fail-=1
    else:
        outp['output'] += 'TEST_6 fail: user login not correctly counted; '

    if loginHelp({'user':'user1', 'password':'password'}) == {'errCode':1, 'count':3}:
        fail-=1
    else:
        outp['output'] += 'TEST_7 fail: user login not correctly counted; '
        
    if loginHelp({'user':'user1', 'password':''}) == {'errCode':-1}:
        fail-=1
    else:
        outp['output'] += 'TEST_8 fail: user authentication implemented incorrectly; '

    if loginHelp({'user':'', 'password':''}) == {'errCode':-1}:
        fail-=1
    else:
        outp['output'] += 'TEST_9 fail: user authentication implemented incorrectly; '

    if loginHelp({'user':'', 'password':'password'}) == {'errCode':-1}:
        fail-=1
    else:
        outp['output'] += 'TEST_8 fail: user authentication implemented incorrectly; '

    outp['nrFailed'] = fail
    return HttpResponse(json.dumps(outp), content_type="application/json")
