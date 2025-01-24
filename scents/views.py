from django.shortcuts import render, get_object_or_404
from django.views.generic.edit import CreateView
from django.contrib.gis import forms

from .models import Scent


class ScentForm(forms.ModelForm):
	class Meta:
		model = Scent
		fields = [
			"loc_gps", "loc_desc", 
			"temperature", "humidity", 
			"was_raining", "was_sunny",
			"weather_note",
			"author",
			"scent_desc",
			"sampling_params",
			"note"
		]
		widgets = {
			"loc_gps": forms.OSMWidget(),
			"author": forms.TextInput(),
			"loc_desc": forms.Textarea(attrs=dict(rows=1)),
			"weather_note": forms.Textarea(attrs=dict(rows=1)),
			"scent_desc": forms.Textarea(attrs=dict(rows=1)),
			"sampling_params": forms.Textarea(attrs=dict(rows=1)),
			"note": forms.Textarea(attrs=dict(rows=1)),
		}


class ScentCreateView(CreateView):
	model = Scent
	form_class = ScentForm


def scent(request, sqid):
	scent = get_object_or_404(Scent, id=Scent.decode_sqid(sqid))
	return render(request, "scents/scent.html", {"object": scent})
