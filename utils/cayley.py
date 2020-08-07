import json
import requests

class CayleyClient:

    entities = {
        'room': '<https://brickschema.org/schema/1.0.3/Brick#Room>',
        'feature': '<http://www.w3.org/ns/mls#Feature>',
        'model': '<http://www.w3.org/ns/mls#Model>'
    }

    def __init__(self, url="http://localhost:64210"):
        self.url = "{}/api/v1/query/gizmo".format(url)

    def count(self, entity_name):
        query = """
            var x = g.V().has('<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>','{}').count();
            g.emit(x);
        """

        entity_uri = self.entities[entity_name]

        resp = requests.post(self.url, data=query.format(entity_uri).encode('utf-8'))
        return resp.json()['result'][0]
