from django.db import models
from django.utils.timezone import now

class Listing(models.Model):
    class JobType(models.TextChoices):
        FULL_TIME = 'Full Time'
        PART_TIME = 'Part Time'

    hr = models.EmailField(max_length=255)
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    company_name = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    description = models.TextField()
    salary = models.IntegerField()
    job_type = models.CharField(max_length=10, choices=JobType.choices, default=JobType.FULL_TIME)
    is_available = models.BooleanField(default=False)
    date_created = models.DateTimeField(default=now)

    def delete(self):
        super().delete()

    def __str__(self):
        return self.title