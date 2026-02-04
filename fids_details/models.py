from django.db import models

class FidsDetail(models.Model):
    device_id = models.CharField(max_length=100, unique=True, verbose_name="Device ID")
    ip_address = models.GenericIPAddressField(unique=True, verbose_name="IP Address")
    mac_address = models.CharField(max_length=17, unique=True, verbose_name="MAC Address")
    location = models.CharField(max_length=255, verbose_name="Location")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.device_id} - {self.location}"

    class Meta:
        verbose_name = "FIDS Detail"
        verbose_name_plural = "FIDS Details"
        ordering = ['device_id']
