from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from . import data

# Create your views here.
def index(request):
    return subjects(request)

def subjects(request):
    template = loader.get_template("SO/index.html")
    subject_data = data.get_data("CON116")
    context = {
        'data': subject_data
    }

    return HttpResponse(template.render(context, request))