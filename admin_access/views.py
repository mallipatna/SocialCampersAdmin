from django.shortcuts import render
from django.http import HttpResponse
from . import models
from dynamodb_mapper.model import ConnectionBorg
from boto.dynamodb.condition import *


# Create your views here.
def createTables(request):
    conn = ConnectionBorg()
    conn.create_table(models.Campground, 1, 1, wait_for_active=True)
    conn.create_table(models.Park, 1, 1, wait_for_active=True)
    conn.create_table(models.Review, 1, 1, wait_for_active=True)
    return HttpResponse("Tables created")


def showCreatePark(request):
    return render(request, 'admin_access/show_create_park.html')


def createPark(request):
    park = models.Park()
    park.parkName = request.POST['parkName'].encode('ascii', 'replace')
    park.about = request.POST['about'].encode('ascii', 'replace')
    park.bestTimeToVisit = request.POST['bestTimeToVisit'].encode('ascii',
                                                                  'replace')
    park.location = request.POST['location'].encode('ascii', 'replace')
    park.placesToGo = request.POST['placesToGo'].encode('ascii', 'replace')
    park.thingsToDo = request.POST['thingsToDo'].encode('ascii', 'replace')
    park.save()
    return HttpResponse("Created park ")


def showParks(request):
    parks = models.Park().scan()
    context = {'park_list': parks}
    return render(request, 'admin_access/show_parks.html', context)


def showPark(request, parkName):
    park = models.Park.get(parkName)
    context = {'park': park}
    return render(request, 'admin_access/show_park.html', context)


def showCampgrounds(request, parkName):
    parkNameCondition = EQ(parkName)
    campgrounds = models.Campground.scan({"parkName": parkNameCondition})
    length = 0
    for campground in campgrounds:
        length = length + 1
    return HttpResponse(length)
    # context = {'campground_list': campgrounds}
    # return render(request, 'admin_access/show_campgrounds.html', context)
