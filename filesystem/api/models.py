from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime


class Region(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"Region: {self.name}"


class County(models.Model):
    name = models.CharField(max_length=100)
    region = models.ForeignKey(Region, related_name='counties', on_delete=models.CASCADE)

    def __str__(self):
        return f"County: {self.name} ({self.region.name})"


class Constituency(models.Model):
    name = models.CharField(max_length=100)
    county = models.ForeignKey(County, related_name='constituencies', on_delete=models.CASCADE)

    def __str__(self):
        return f"Constituency: {self.name} ({self.county.name})"


class Project(models.Model):
    STATUS_CHOICES = [
        ('not_started', 'Not Started'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
    ]

    rfx_number = models.BigIntegerField(primary_key=True)  # Unique identifier
    name = models.CharField(max_length=100)
    constituency = models.ForeignKey(Constituency, related_name='projects', on_delete=models.CASCADE)
    contracting_company = models.CharField(max_length=255)
    contract_date = models.DateField(default=datetime.date.today)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not_started')

    def __str__(self):
        return f"Project: {self.name} (RFX: {self.rfx_number})"


class File(models.Model):
    name = models.CharField(max_length=100)
    file = models.FileField(upload_to='')
    project = models.ForeignKey(Project, related_name='files', on_delete=models.CASCADE)

    def __str__(self):
        return f"File: {self.name} (Project: {self.project.name}, Contractor: {self.project.contracting_company})"

    def get_absolute_url(self):
        return self.file.url


class User(AbstractUser):
    ROLE_CHOICES = [
        ('super_admin', 'Super Admin'),
        ('admin', 'Admin'),
        ('basic_user', 'Basic User'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='basic_user')

    def save(self, *args, **kwargs):
        # Only override role if it wasn't set explicitly
        if not self.role:
            if self.is_superuser:
                self.role = "super_admin"
            elif self.is_staff:
                self.role = "admin"
            else:
                self.role = "basic_user"

        super().save(*args, **kwargs)
