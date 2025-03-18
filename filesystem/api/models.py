from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime
from django.utils.timezone import now

class User(AbstractUser):
    ROLE_CHOICES = [
        ('Super admin', 'Super Admin'),
        ('Admin', 'Admin'),
        ('Basic', 'Basic User'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='basic_user')

    def save(self, *args, **kwargs):
        if not self.role:  # ✅ Only set if empty
            if self.is_superuser:
                self.role = "Super Admin"
            elif self.is_staff:
                self.role = "Admin"
            else:
                self.role = "Basic"

        super().save(*args, **kwargs)

class Region(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"Region: {self.name}"


class County(models.Model):
    name = models.CharField(max_length=100)
    region = models.ForeignKey(Region, related_name='counties', on_delete=models.PROTECT)

    def __str__(self):
        return f"County: {self.name} ({getattr(self.region, 'name', 'No Region')})"


class Constituency(models.Model):
    name = models.CharField(max_length=100)
    county = models.ForeignKey(County, related_name='constituencies', on_delete=models.PROTECT)

    def __str__(self):
        return f"Constituency: {self.name} ({getattr(self.county, 'name', 'No County')})"


class Project(models.Model):
    STATUS_CHOICES = [
        ('Not Started', 'Not Started'),
        ('Ongoing', 'Ongoing'),
        ('Completed', 'Completed'),
    ]
    id = models.AutoField(primary_key=True)
    rfx_number = models.BigIntegerField(unique=True)  # Unique identifier
    name = models.CharField(max_length=100)
    constituency = models.ForeignKey(Constituency, related_name='projects', on_delete=models.PROTECT)
    contracting_company = models.CharField(max_length=255)
    contract_date = models.DateField(default=datetime.date.today)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Not Started')

    def __str__(self):
        return f"Project: {self.name} (RFX: {self.rfx_number})"


class File(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="files")
    file = models.FileField(upload_to="project_files/")
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    upload_date = models.DateTimeField(auto_now_add=True)
    size = models.PositiveBigIntegerField(default=0)
    name = models.CharField(max_length=255)

    def save(self, *args, **kwargs):
        """Auto-fill size and name on save."""
        if not self.name:
            self.name = self.file.name  # Default to uploaded filename
        self.size = self.file.size  # Get file size
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.project.rfx_number})"