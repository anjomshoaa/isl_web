from django.shortcuts import render

#from django.http import HttpResponse
#from django.template import loader
#from .models import Question

from utils.cayley import CayleyClient



def rooms(request):
    latest_question_list = ['Q1', 'Q2', 'Q3']

    client = CayleyClient()

    context = {
        'rooms': client.list_rooms(),
        'title': 'Space information',
    }
    return render(request, 'graph/rooms.html', context)


"""
var sensor_path = g.Morphism()
.in('<rdfs:subClassOf>')
	.tag("name")
.in('<rdf:type>');

g.V('<brick:Sensor>')
.in('<rdfs:subClassOf>')
	.tag("sensor_type")
	.out('<rdfs:label>')
	.tag('sensor_name')
	.back('sensor_type')

	.in('<rdf:type>')
.has('<bf:isPointOf>', '<isl:/rooms/1>')
	.tag("sensor_id")

	.out('<bf:hasMeasurement>')
	.tag('csv_file')
	.all()
"""



"""
g.V('<isl:/rooms/2>').out(null, "pred").all()


g.V("<brick:Room>").in("<rdf:type>").ForEach(function(v) {
  //g.emit(v.room)
  var props = g.V(v.id).out(null, "pred").ToArray()
  var node = {"room": v.id, "props": props}
  g.emit(node)
})



"""
