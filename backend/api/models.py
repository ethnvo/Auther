from django.db import models

class Paper(models.Model):
    title = models.CharField(max_length=255)
    abstract = models.TextField()
    authors = models.JSONField()  # e.g. ["Alice Smith", "John Doe"]
    date = models.DateField(null=True, blank=True)
    has_woman_author = models.BooleanField(default=False)
    link = models.URLField(blank=True)
    gender_inference_possible = models.BooleanField(default=True)


    def __str__(self):
        return self.title
    
