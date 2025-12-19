from django.db import models

class PhoneExtension(models.Model):
    name = models.CharField(max_length=100)
    extension_number = models.CharField(max_length=20, verbose_name="Extension Number")
    full_number = models.CharField(max_length=50, blank=True, null=True, verbose_name="Full Number")

    def __str__(self):
        return f"{self.name} - {self.extension_number}"
