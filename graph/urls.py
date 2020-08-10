from django.urls import path

from . import views
#from isl import views as isl_views

# app_name = 'features'

urlpatterns = [
    path('', views.rooms, name='rooms'),

    #path('rooms/', views.rooms, name='rooms'),
    path('<path:room_id>/sensors', views.sensors, name='sensors'),
    #path('<path:room_id>/sensors/<path:sensor_id>/data/<str:file_name>', isl_views.data_viewer, name='sensors'),

    # datasets, tasks, models, runs
    path('entities/<str:entity_type>', views.entities, name='entities'),

]
