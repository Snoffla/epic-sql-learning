from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse

from sqlalchemy import create_engine, desc
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
    order = request.GET.get('order')

    query = session.query(Person)

    if(shirt_or_hat):
        query = query.filter(Person.shirt_or_hat == shirt_or_hat)
    
    if(team):
        query = query.filter(getattr(Person, "team") == team)
    
    print(order)

    if(order):
        if order[0] == '-':
            query = query.order_by(desc(getattr(Person, order[1:])))
        else:
            query = query.order_by(getattr(Person, order))
    
    people = list(query)

    return JsonResponse([person.as_dict() for person in people], safe=False)