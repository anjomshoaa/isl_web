from django.shortcuts import render

#from django.http import HttpResponse
#from django.template import loader
#from .models import Question

from utils.cayley import CayleyClient



def rooms(request):

    client = CayleyClient()

    context = {
        'rooms': client.list_entities('room'),
        'title': 'Space information',
    }
    return render(request, 'graph/rooms.html', context)



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
