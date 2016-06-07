from django.db import models

# Create your models here.
class Url(models.Model):
    path = models.CharField(max_length=255)
    title = models.TextField()

    def get_absolute_url(self):
        return reverse('url_edit', kwargs={'pk': self.pk})
