from django.db import models


class System(models.Model):
    name = models.CharField(max_length=200, unique=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Location(models.Model):
    name = models.CharField(max_length=200, unique=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Credential(models.Model):
    system = models.ForeignKey(System, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.CharField(max_length=255)
    username = models.CharField(max_length=200, blank=True, null=True)
    password = models.CharField(max_length=200, blank=True, null=True)
    ipv4 = models.GenericIPAddressField(protocol='IPv4', blank=True, null=True, verbose_name="IPv4")
    subnet_mask = models.GenericIPAddressField(protocol='IPv4', blank=True, null=True)
    gateway = models.GenericIPAddressField(protocol='IPv4', blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='credentials/', blank=True, null=True)

    def __str__(self):
        return f"{self.system} - {self.username}"
