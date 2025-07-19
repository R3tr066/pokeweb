from django.db import models

class Set(models.Model):
    set_id = models.CharField(max_length=10)
    name = models.CharField(max_length=20)
    series = models.CharField(max_length=50, blank=True, null=True)
    printed_total = models.IntegerField(blank=True, null=True)
    total = models.IntegerField(blank=True, null=True)
    ptc_code = models.CharField(max_length=10, blank=True, null=True)
    release_date = models.DateField(blank=True, null=True)
    updated_at = models.DateField(blank=True, null=True)
    symbol = models.CharField(max_length=255, blank=True, null=True)
    logo = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name