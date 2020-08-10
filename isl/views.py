from django.shortcuts import render

#from django.http import HttpResponse
#from django.template import loader
#from .models import Question

from utils.cayley import CayleyClient

import pandas as pd
import tensorflow as tf


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


def model_viewer(request, file_name):

    MODEL_PATH = '/Users/amin/pyworks/notebooks/isl_occupancy/'
    #clean_name = file_name.split(':')[1][:-1]
    print(MODEL_PATH + file_name)

    tf_model = tf.keras.models.load_model(MODEL_PATH + file_name)

    context = {
        'title': 'Model Viewer ' + file_name,
        'model_summary': tf_model.to_json()
    }
    return render(request, 'isl/model_viewer.html', context)
