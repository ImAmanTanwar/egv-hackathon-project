from django.shortcuts import render
import json,requests
from models import Categories,SubCategories,Complains
from .utilities import MapObj
from django.http import HttpResponse
import os
# Create your views here.

def test(request):
    context={}
    all_entries = Complains.objects.all()
    obj_list=[]
    for i in all_entries:
        mapobj = MapObj()
        mapobj.lat=i.lat
        mapobj.lon=i.lon
        try:
            mapobj.c_id = SubCategories.objects.get(service_code=str(i.service_code)).group_id.c_id
        except:
            mapobj.cid = 1
        obj_list.append(mapobj)
    for j in obj_list:
        print j.lat
    context["data"]=obj_list
    context["googlemapskey"] = os.environ["GOOGLE_MAPS_KEY"]
    return render(request,"test.html",context)
