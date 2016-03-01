from django.shortcuts import render
from django.http import HttpResponse
# . implies current directory
from . import models
from dynamodb_mapper.model import ConnectionBorg
from boto.dynamodb.condition import *
from decimal import Decimal


# Create your views here.
def createTables(request):
    conn = ConnectionBorg()
    conn.create_table(models.Campground, 1, 1, wait_for_active=True)
    #conn.create_table(models.Park, 1, 1, wait_for_active=True)
    #conn.create_table(models.Review, 1, 1, wait_for_active=True)
    return HttpResponse("Tables created")


def showCreatePark(request):
    return render(request, 'admin_access/show_create_park.html')


def showCreateCampground(request):
    return render(request, 'admin_access/show_create_campground.html')


# method to create campground
# Display all parks in a drop-down and then select a park and enter campground information.
def createCampground(request):
    #parks = models.Park().scan()
    #context = {'park_list': parks}
    #render(request,'admin_access/show_create_campground.html', context)
    #context = {'park_list': parks}
    #return render(request, 'admin_access/show_parks.html', context)
    campground = models.Campground()
    campground.parkName = request.POST['parkName']
    campground.campgroundName = request.POST['campgroundName']
    #campground.parkCampgroundName = campground.parkName + "::" + campground.campgroundName
    campground.bathroomType = request.POST['bathroomType']
    campground.datesOpen = request.POST['datesOpen']
    campground.dumpStation = toBoolean(request.POST['dumpStation'])
    campground.fee = Decimal(request.POST['fee'])
    campground.numberCampsites = int(request.POST['numberCampsites'])
    campground.reserveSite = toBoolean(request.POST['reserveSite'])
    campground.rvHookup = toBoolean(request.POST['rvHookup'])
    campground.shower = toBoolean(request.POST['shower'])
    campground.save()
    return HttpResponse("Created campground")


def toBoolean(uc):
    if (uc == u"true") or (uc == u"yes") or (uc == u"True") or (uc == u"Yes"):
        return True
    else:
        return False


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
