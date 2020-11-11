cayley http --load /Users/amin/pyworks/isl_web/graph/building_model.nq
cayley http --load /Users/amin/pyworks/notebooks/isl_occupancy/ontology/building_model_1.nq 

conda activate django
python manage.py runserver
