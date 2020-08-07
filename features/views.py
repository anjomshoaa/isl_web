from django.shortcuts import render

#from django.http import HttpResponse
#from django.template import loader
#from .models import Question


def index(request):
    latest_question_list = ['Q1', 'Q2', 'Q3']
    context = {
        'latest_question_list': latest_question_list,
    }
    return render(request, 'features/index.html', context)
