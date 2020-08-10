import json
import requests

class CayleyClient:

    entities = {
        'room': '<brick:Room>',
        'feature': '<mls:Feature>',
        'model': '<mls:Model>',
        'dataset': '<mls:Dataset>',
        'task': '<mls:Task>',
        'run': '<mls:Run>',
    }

    def __init__(self, url="http://localhost:64210"):
        self.url = "{}/api/v1/query/gizmo".format(url)

    def count(self, entity_name):
        query = """
            var x = g.V().has('<rdf:type>','{}').count();
            g.emit(x);
        """

        entity_uri = self.entities[entity_name]

        resp = requests.post(self.url, data=query.format(entity_uri).encode('utf-8'))
        return resp.json()['result'][0]


    """ load instances of given class and all their properties
    """
    def __get_instances(self, class_uri):
        query = """
              g.V('{}').in("<rdf:type>").ForEach(function(entity) {{
              g.V(entity.id).out(null, "property").ForEach(function (elm){{
                g.emit({{"value": elm.id, "property": elm.property, "entity":entity.id}});
              }})
            }})
        """
        data = requests.post(self.url, data=query.format(class_uri).encode('utf-8')).json()

        entities = {}
        if 'result' in data:
            for elm in data['result']:

                entity, property, value = elm.values()
                entity_id = entity.split(':')[1][:-1]

                if entity_id not in entities:
                    entities[entity_id] = {'properties': []}

                entities[entity_id]['properties'].append([property, value])
                #append({'property': property, 'value': value})

        #print(entities)
        # sort on property names
        for entity_id in entities:
            properties = entities[entity_id]['properties']
            entities[entity_id]['properties'] = sorted(properties, key=lambda rec: rec[0])

        return entities


    def list_entities(self, entity_name):
        return self.__get_instances(self.entities[entity_name])

    def room_sensors(self, room_id):
        query = """
            g.V('<brick:Sensor>')
                .in('<rdfs:subClassOf>').tag("sensor_type")
	            .out('<rdfs:label>').tag('sensor_name')
	            .back('sensor_type')
	            .in('<rdf:type>')
                .has('<bf:isPointOf>', '<isl:/{}>').tag("sensor_id")
                .out('<bf:hasMeasurement>').tag('csv_file').all()
        """

        resp = requests.post(self.url, data=query.format(room_id).encode('utf-8'))
        return resp.json()['result']
