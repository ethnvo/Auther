from django.db import models
from django.conf import settings

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
    
class Favorite (models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="favorites"
    )
    paper = models.ForeignKey(Paper, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)

    class Meta:
        unique_together = ("user", "paper")

class RecentlyViewed(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="recent_views"
    )
    paper = models.ForeignKey(Paper, on_delete=models.CASCADE)
    viewed_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("user", "paper")
        ordering = ["-viewed_at"]