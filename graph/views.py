from django.shortcuts import render

#from django.http import HttpResponse
#from django.template import loader
#from .models import Question

from utils.cayley import CayleyClient


def clean_name(entity, length=-1):
    return entity.split(':')[1][:length]

def rooms(request):

    client = CayleyClient()

    context = {
        'rooms': client.list_entities('room'),
        'title': 'Space information',
    }
    return render(request, 'graph/rooms.html', context)


def evaluations(request):

    client = CayleyClient()
    task_name = 'occupancy_task'
    results = client.task_evaluations(task_name)

    evals={}
    labels = []

    for elm in results:

        name = clean_name(elm['metric_name'])
        model_id = clean_name(elm['model_id'], 9)
        learning_task = clean_name(elm['learning_task'])
        val = float(elm['metric_value'].split('"')[1])

        labels.append(model_id)

        if name not in evals:
            evals[name] = {}

        if learning_task not in evals[name]:
            evals[name][learning_task] = []

        evals[name][learning_task].append({
            'x': val,
            'y': model_id,
            'run': clean_name(elm['run_id'], 7)
        })


    metrics = {}
    for metric_name, learning_tasks in evals.items():
        metrics[metric_name] = []
        for task, data in learning_tasks.items():
            metrics[metric_name].append({'label': task, 'data': data})


    context = {
        'title': 'Task Evaluation: ' + task_name,
        'labels': list(set(labels)),
        'metrics': metrics
    }
    return render(request, 'graph/evaluations.html', context)




def sensors(request, room_id):

    client = CayleyClient()

    sensors = client.room_sensors(room_id)
    for sensor in sensors:
        sensor['stream'] = ('ws://' in sensor['resource'])

    context = {
        'sensors': sensors,
        'title': 'Sensors in <' + room_id + '>',
    }
    return render(request, 'graph/sensors.html', context)


def entities(request, entity_type):

    client = CayleyClient()
    entities = client.list_entities(entity_type)


    # add entity-specific buttons
    if entity_type == 'model':
        for name, data in entities.items():
            data['buttons'] = []
            hyperlink = ''
            for prop in data['properties']:
                if prop[0] == '<dcterms:identifier>':
                    data['buttons'].append(['View model', '/model/'+prop[1]])

    if entity_type == 'room':
        for name, data in entities.items():
            data['buttons'] = [['Sensors', '/graph' + name + '/sensors' ]]


    print(entities)

    context = {
        'entities': entities,
        'title': entity_type.capitalize() + ' information',
    }
    return render(request, 'graph/entities.html', context)
