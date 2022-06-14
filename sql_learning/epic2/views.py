from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse

from sqlalchemy import create_engine, desc, asc
from sqlalchemy.orm import sessionmaker
from epic2.db_models import *

from django.http import JsonResponse
import json
import math

page_size = 25

class Col:
    def __init__(self, display_name, col_id):
        self.display_name = display_name
        self.col_id = col_id

def index(request):
    session = get_db_session()
    shirt_or_hat = request.GET.get('shirt_or_hat')
    team = request.GET.get('team')

    teams = [team for team, in session.query(Person.team).distinct(Person.team)]

    template = loader.get_template('base.html')
    context = {
        'team_list': teams,
        'shirt_or_hat': shirt_or_hat,
        'columns': [
            Col("First name", "first_name"),
            Col("Last name", "last_name"),
            Col("Shirt or Hat", "shirt_or_hat"),
            Col("Points", "quiz_points"),
            Col("Team", "team"),
            Col("Age", "age"),
            Col("Sign up", "signup"),
            Col("State", "state_name")
        ] 
    }
    return HttpResponse(template.render(context, request))


def api(request):
    session = get_db_session()
    shirt_or_hat = request.GET.get('shirt_or_hat')
    team = request.GET.get('team')
    order = request.GET.get('order')
    page = request.GET.get('page')

    page = page if page else "0"

    query = session.query(Person, State).outerjoin(State, Person.state_code == State.state_abbrev)

    if(shirt_or_hat):
        query = query.filter(Person.shirt_or_hat == shirt_or_hat)
    
    if(team):
        query = query.filter(getattr(Person, "team") == team)
    
    print(order)

    if(order):
        attr, sort = (order[1:], desc) if order[0] == '-' else (order, asc)
        obj = Person if hasattr(Person, attr) else State 
        query = query.order_by(sort(getattr(obj, attr)))

    rows = query.count()
    query = query.limit(page_size).offset(page_size*int(page))
    
    people = list(query)
    print(people)

    return JsonResponse({
        "count": math.ceil(rows/page_size),
        "people": [{**person.as_dict(), **state.as_dict()} for person, state in people]}
        , safe=False)