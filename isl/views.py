from django.shortcuts import render

#from django.http import HttpResponse
#from django.template import loader
#from .models import Question

import isl.settings as settings
from utils.cayley import CayleyClient

import pandas as pd
import tensorflow as tf
from web3 import Web3

def dashboard(request):

    client = CayleyClient()

    context = {
        'title': 'Basic statistics',
        'no_rooms': client.count('room'),
        'no_models': client.count('model'),
        'no_features': client.count('feature')
    }
    return render(request, 'isl/dashboard.html', context)


def data_viewer(request, file_name):

    DATA_PATH = '/Users/amin/Downloads/Dataset/filleddata/'
    clean_name = file_name.split(':')[1][:-1]

    data_frame = pd.read_csv(DATA_PATH + clean_name, nrows=100)

    context = {
        'title': 'Data Viewer ' + file_name,
        'data_frame': data_frame
    }
    return render(request, 'isl/data_viewer.html', context)


def chart_viewer(request, mqtt_url):

    broker, tail = mqtt_url.replace('ws://', '').split(':')
    port, topic = tail.split('/', 2)
    print(broker, tail, port, topic)
    context = {
        'title': 'Sensor data stream',
        'mqtt_broker': broker,
        'mqtt_port': port,
        'mqtt_topic': '/'+topic
    }

    return render(request, 'isl/chart_viewer.html', context)


def model_viewer(request, file_name):

    MODEL_PATH = '/Users/amin/pyworks/notebooks/isl_occupancy/model/'
    #clean_name = file_name.split(':')[1][:-1]
    print(MODEL_PATH + file_name)

    tf_model = tf.keras.models.load_model(MODEL_PATH + file_name)

    context = {
        'title': 'Model Viewer ' + file_name,
        'model_summary': tf_model.to_json()
    }
    return render(request, 'isl/model_viewer.html', context)


def account_viewer(request):
    provider = Web3(Web3.HTTPProvider(settings.W3_PROVIDER))
    context = {
        'accounts': provider.eth.accounts
        }
    return render(request, 'isl/account_viewer.html', context)
