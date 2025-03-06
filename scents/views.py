from django.shortcuts import render, get_object_or_404
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.gis import forms
from django.forms import inlineformset_factory

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from .models import User, Scent, Attachment


class ScentForm(forms.ModelForm):
	user = forms.ModelChoiceField(label=Scent._meta.get_field("user").verbose_name.title(), queryset=User.objects.all(), disabled=True)

	class Meta:
		model = Scent
		fields = [
			"name",
			"author",
			"user",
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


AttachmentFormSet = inlineformset_factory(Scent, Attachment, fields=["file", "note"], extra=0, can_delete=True, widgets={"note": forms.Textarea(attrs=dict(rows=1, placeholder="Enter comment"))})


class ScentCreateView(LoginRequiredMixin, CreateView):
	model = Scent
	form_class = ScentForm

	def get_context_data(self, **kwargs):
		data = super().get_context_data(**kwargs)
		if self.request.POST:
			data["attachments"] = AttachmentFormSet(self.request.POST, self.request.FILES)
		else:
			data["attachments"] = AttachmentFormSet()
		return data

	def get_form_kwargs(self):
		kwargs = super().get_form_kwargs()
		kwargs.update({"initial": dict(user=self.request.user)})
		return kwargs

	def form_valid(self, form):
		context = self.get_context_data()
		attachments = context["attachments"]

		if attachments.is_valid():
			self.object = form.save()
			attachments.instance = self.object
			attachments.save()

		return super().form_valid(form)


class ScentUpdateView(LoginRequiredMixin, UpdateView):
	model = Scent
	form_class = ScentForm

	def get_object(self):
		sqid = self.kwargs.get("sqid")
		return get_object_or_404(self.model, id=self.model.decode_sqid(sqid))

	def get_context_data(self, **kwargs):
		data = super().get_context_data(**kwargs)
		if self.request.POST:
			data["attachments"] = AttachmentFormSet(self.request.POST, self.request.FILES, instance=self.object)
		else:
			data["attachments"] = AttachmentFormSet(instance=self.object)
		return data

	def get_form_kwargs(self):
		kwargs = super().get_form_kwargs()
		kwargs.update({"initial": dict(user=self.request.user)})
		return kwargs

	def form_valid(self, form):
		context = self.get_context_data()
		attachments = context["attachments"]

		if attachments.is_valid():
			self.object = form.save()
			attachments.instance = self.object
			attachments.save()

		return super().form_valid(form)

@login_required
def scent(request, sqid):
	scent = get_object_or_404(Scent, id=Scent.decode_sqid(sqid))
	return render(request, "scents/scent.html", {"object": scent})
