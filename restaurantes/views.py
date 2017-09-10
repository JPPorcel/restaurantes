# -*- coding: utf-8 -*-

from django.shortcuts import render, HttpResponse, redirect, Http404
from restaurantes.models import restaurants
from restaurantes.forms import RestaurantForm
import requests
from random import randint
from mongoengine.connection import get_db
from gridfs import GridFS, NoFile
from bson.objectid import ObjectId
from django.contrib.auth.decorators import login_required
import urllib, json
from django.http import JsonResponse
from io import BytesIO
from PIL import Image

API_KEY = "%20AIzaSyAlWonn1P-PzadEBz3VWybVtjasLLxSDns"

# Create your views here.

def index(request):
	context = {}   # Aqui van la las variables para la plantilla
	return render(request,'index.html', context)

def listar(request):
	context = {
		"restaurantes": restaurants.objects[:20], # los veinte primeros
		"menu": "listar",
	}
	return render (request, 'listar.html', context)

def serve_file(request, file_id):
	db = get_db()
	fs = GridFS(db)
	try:
		f = fs.get(ObjectId(file_id))
	except NoFile:
		fs = GridFS(db, collection='images') # mongoengine stores images in a separate collection by default
		try:
			f = fs.get(ObjectId(file_id))
		except NoFile:
			raise Http404
		
	response = HttpResponse(f.read(), content_type=f.content_type)
	# add other header data like etags etc. here
	return response

def restaurante(request, id):
	r = restaurants.objects(restaurant_id=str(id)).first()

	context = {
		"restaurante": r,
	}   # Aqui van la las variables para la plantilla
	return render (request, 'restaurante.html', context)

def parseURL(addr):
	addr = addr.encode('utf-8')
	addr = addr.replace("á","a")
	addr = addr.replace("é","e")
	addr = addr.replace("í","i")
	addr = addr.replace("ó","o")
	addr = addr.replace("ú","u")
	addr = addr.replace("ñ","n")
	return addr

@login_required(login_url='/accounts/login/')
def getPhoto(request, address):
	url = "https://maps.googleapis.com/maps/api/streetview?size=800x600&location="+address+"&key="+API_KEY
	return HttpResponse(urllib.urlopen(url).read(), content_type="image/jpeg")

def getCity(request, city):
	url = "https://maps.googleapis.com/maps/api/place/autocomplete/json?input="+city+"&types=(cities)&language=es&key="+API_KEY
	response = urllib.urlopen(url)
	data = json.loads(response.read())
	cities=[]
	for c in data["predictions"]:
		cities.append(c["description"])
	return JsonResponse(cities, safe=False)

def getAddress(request, name):
	url = "http://maps.googleapis.com/maps/api/geocode/json?address="+name+"&language=es"
	response = urllib.urlopen(url)
	data = json.loads(response.read())
	print(data)
	address=[]
	for c in data["results"]:
		address.append(c["formatted_address"])
	if len(address) == 0:
		address.append("error")
	return JsonResponse(address[0], safe=False)

@login_required(login_url='/accounts/login/')
def add(request):
	if request.method == 'GET':
		formulario = RestaurantForm()
		# GET
		context = {
			'formulario': formulario,
			"menu": "add",
		}   # Aqui van la las variables para la plantilla
		return render(request, 'add.html', context)

	if request.method == 'POST':
		formulario = RestaurantForm(request.POST, request.FILES)
		formulario.is_valid()
		name = formulario.cleaned_data.get('name')
		cuisine = formulario.cleaned_data.get('cuisine')
		borough = formulario.cleaned_data.get('borough')
		city = formulario.cleaned_data.get('city')
		address = formulario.cleaned_data.get('address')
		image_default = formulario.cleaned_data.get('image_default')
		if(image_default == "yes"):
			URL = "https://maps.googleapis.com/maps/api/streetview?size=800x600&location="+address+"&key="+API_KEY
			URL = parseURL(URL)
			image = BytesIO(urllib.urlopen(URL).read())
		else:
			image = request.FILES.get('image_file')

		# crear id aleatorio, un numero de 8 cifras y que no se encuentre ya en la base de datos
		restaurant_id = randint(10000000,99999999)
		while(restaurants.objects(restaurant_id=str(restaurant_id)).first() != None):
			restaurant_id = randint(10000000,99999999)

		if(name != "" and cuisine != "" and borough != "" and city != "" and address != ""):
			r = restaurants(name=name, restaurant_id=str(restaurant_id), cuisine=cuisine, borough=borough, city=city, address=address, image=image)
			r.save()
			return redirect('restaurante', id=restaurant_id)
        
	


def search(request):
	context = {
		"restaurantes": restaurants.objects(cuisine__icontains=request.GET.get('cocina')),
	}
	return render (request, 'listar.html', context)
