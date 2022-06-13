from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from epic2.db_models import *

from django.http import JsonResponse
import json


def index(request):
    session = get_db_session()
    shirt_or_hat = request.GET.get('shirt_or_hat')
    team = request.GET.get('team')

    teams = [team for team, in session.query(Person.team).distinct(Person.team)]
    query = session.query(Person).order_by(Person.first_name)

    if(shirt_or_hat):
        query = query.filter(Person.shirt_or_hat == shirt_or_hat)
    
    if(team):
        query = query.filter(Person.team == team)
    
    people = list(query)

    template = loader.get_template('base.html')
    context = {
        'person_list': people,
        'team_list': teams,
        'shirt_or_hat': shirt_or_hat
    }
    return HttpResponse(template.render(context, request))

def api(request):
    session = get_db_session()
    shirt_or_hat = request.GET.get('shirt_or_hat')
    team = request.GET.get('team')

    query = session.query(Person).order_by(Person.first_name)

    if(shirt_or_hat):
        query = query.filter(Person.shirt_or_hat == shirt_or_hat)
    
    if(team):
        query = query.filter(Person.team == team)
    
    people = list(query)
    print(people[0].as_dict())

    return JsonResponse([person.as_dict() for person in people], safe=False)