from django.contrib.gis.db import models
from django.contrib.auth.models import User
from django.urls import reverse

from sqids import Sqids


class ScentQuerySet(models.QuerySet):
    def get_by_sqid(self, sqid):
        return self.filter(id=self.model.decode_sqid(sqid))


class Scent(models.Model):
    # Location
    loc_gps = models.PointField(verbose_name="GPS location")
    loc_desc = models.TextField(verbose_name="Location description")

    # Weather
    temperature = models.FloatField(verbose_name="Temperature [°C]")
    humidity = models.FloatField(verbose_name="Humidity")
    was_raining = models.BooleanField(verbose_name="Raining?")
    was_sunny = models.BooleanField(verbose_name="Sunny?")

    weather_note = models.TextField(verbose_name="Weather note", blank=True)

    # Scent data
    name = models.TextField(verbose_name="Scent name")
    author = models.TextField(verbose_name="Author")
    user = models.ForeignKey(User, verbose_name="User", on_delete=models.SET_NULL, blank=True, null=True)
    
    scent_desc = models.TextField(verbose_name="Scent description")
    sampling_params = models.TextField(verbose_name="Sampling parameters", blank=True)

    # Special
    note = models.TextField(blank=True)

    # Ids
    sqids = Sqids(blocklist=[], min_length=5)

    @property
    def sqid(self):
        return self.sqids.encode([self.id])

    @classmethod
    def decode_sqid(cls, sqid: str):
        return cls.sqids.decode(sqid)[0]

    def __str__(self):
        return self.sqid

    def get_absolute_url(self):
        return reverse("scent-view", args=[self.sqid])

    objects = models.Manager.from_queryset(ScentQuerySet)


class Attachment(models.Model):
    def upload_to(instance, filename):
        return "{}/{}".format(instance.scent.sqid, filename)

    scent = models.ForeignKey(Scent, related_name="attachments", on_delete=models.CASCADE)

    file = models.FileField(upload_to=upload_to)
    note = models.TextField(blank=True, verbose_name="Note")


from django.db.models.signals import post_delete
from django.dispatch.dispatcher import receiver
@receiver(post_delete, sender=Attachment)
def attachment_delete(sender, instance, **kwargs):
    if instance.file:
        instance.file.delete(False)
