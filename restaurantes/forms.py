# -*- coding: utf-8 -*-
from django import forms

class RestaurantForm(forms.Form):
	
	city = forms.CharField(required=True, label="Ciudad")
	name = forms.CharField(required=True, max_length=80, label="Nombre")
	cuisine = forms.CharField(required=True, label="Cocina")
	borough = forms.CharField(required=True, label="Situación")
	address = forms.CharField(required=True, label="Dirección")
	image = forms.ImageField(label="Imagen", help_text="600x600px")
	image_default = forms.CharField(label="Imagen por Defecto", initial="no")
