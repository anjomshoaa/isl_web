from django.shortcuts import render

#from django.http import HttpResponse
#from django.template import loader
#from .models import Question

from utils.cayley import CayleyClient


def dashboard(request):

    client=CayleyClient()

    latest_question_list = ['Q1', 'Q2', 'Q3']
    context = {
        'latest_question_list': latest_question_list,
        'title': 'Space Information',
        'no_rooms': client.count('room'),
        'no_models': client.count('model'),
        'no_features': client.count('feature')
    }
    return render(request, 'isl/dashboard.html', context)
