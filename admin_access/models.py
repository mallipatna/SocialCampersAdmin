from __future__ import unicode_literals
from dynamodb_mapper.model import DynamoDBModel, autoincrement_int
from django.db import models
from decimal import Decimal
import datetime


# Create your models here.
class Park(DynamoDBModel):
    __table__ = "Park"
    __hash_key__ = "parkName"
    __schema__ = {
        "parkName": str,
        "about": str,
        "bestTimeToVisit": str,
        "location": str,
        "placesToGo": str,
        "thingsToDo": str,
    }


class Campground(DynamoDBModel):
    __table__ = "Campground"
    __hash_key__ = "parkName"
    __range_key__ = "campgroundName"
    __schema__ = {
        "parkName": unicode,
        "campgroundName": unicode,
        "bathroomType": unicode,
        "datesOpen": unicode,
        "dumpStation": bool,
        "fee": Decimal,
        "numberCampsites": int,
        "reserveSite": bool,
        "rvHookup": bool,
        "shower": bool,
    }


class Review(DynamoDBModel):
    __table__ = "Review"
    __hash_key__ = "reviewId"
    __schema__ = {
        "reviewId": autoincrement_int,
        "parkCampgroundName": str,
        "parkName": str,
        "campgroundName": str,
        "reviewText": str,
        "rating": int,
        "user": str,
        "date": datetime,
    }
