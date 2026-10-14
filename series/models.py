from django.db import models

class Franchise(models.Model):
    name = models.CharField(max_length=100, unique=True)
    production_company = models.CharField(max_length=100)
    creation_year = models.IntegerField()

    class Meta:
        verbose_name_plural = "Franchises"

    def __str__(self):
        return self.name
    
class Series(models.Model):
    PLATFORMS = [
        ('TV', 'TV Broadcast'),
        ('TTFC', 'Toei Tokusatsu Fan Club'),
        ('PRIME', 'Amazon Prime Video'),
        ('WEB', 'Web Streaming'),
        ('OTHER', 'Other Plataform'),
    ]
    franchise = models.ForeignKey(Franchise, on_delete=models.CASCADE, related_name='series')
    base_series = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='spin_offs')
    title = models.CharField(max_length=150, unique=True)
    platform = models.CharField(max_length=20, choices=PLATFORMS, default='TV')
    release_year = models.IntegerField()
    episode_count = models.IntegerField(null=True, blank=True)
    theme = models.CharField(max_length=100)
    is_airing = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Series"

    def __str__(self):
        series_type = "Spin Off" if self.base_series else "Main"
        return f"{self.title} [{series_type}]"