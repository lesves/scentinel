from django.shortcuts import render, get_object_or_404
from django.views.generic.edit import CreateView
from django.contrib.gis import forms
from django.forms import inlineformset_factory

from .models import Scent, Attachment


class ScentForm(forms.ModelForm):
	class Meta:
		model = Scent
		fields = [
			"name",
			"author",
			"scent_desc",
			"sampling_params",

			"loc_gps", "loc_desc", 

			"temperature", "humidity", 
			"was_raining", "was_sunny",
			"weather_note",

			"note"
		]
		widgets = {
			"loc_gps": forms.OSMWidget(),
			"name": forms.TextInput(),
			"author": forms.TextInput(),
			"loc_desc": forms.Textarea(attrs=dict(rows=1)),
			"weather_note": forms.Textarea(attrs=dict(rows=1)),
			"scent_desc": forms.Textarea(attrs=dict(rows=1)),
			"sampling_params": forms.Textarea(attrs=dict(rows=1)),
			"note": forms.Textarea(attrs=dict(rows=1)),
		}


AttachmentFormSet = inlineformset_factory(Scent, Attachment, fields=["file", "note"], extra=0, can_delete=False, widgets={"note": forms.Textarea(attrs=dict(rows=1))})


class ScentCreateView(CreateView):
	model = Scent
	form_class = ScentForm

	def get_context_data(self, **kwargs):
		data = super().get_context_data(**kwargs)
		if self.request.POST:
			data["attachments"] = AttachmentFormSet(self.request.POST, self.request.FILES)
		else:
			data["attachments"] = AttachmentFormSet()
		return data

	def form_valid(self, form):
		context = self.get_context_data()
		attachments = context["attachments"]

		if attachments.is_valid():
			self.object = form.save()

			for attachment in attachments:
				attachment.scent = self.object
			attachments.save()

		return super().form_valid(form)


def scent(request, sqid):
	scent = get_object_or_404(Scent, id=Scent.decode_sqid(sqid))
	return render(request, "scents/scent.html", {"object": scent})
