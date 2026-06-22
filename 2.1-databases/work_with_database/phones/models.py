from django.db import models
from django.utils.text import slugify

class Phone(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255) # название модели телефона
    price = models.IntegerField() # цена телефона
    image = models.URLField() # ссылка на изображение телефона
    release_date = models.DateField() # дата выхода модели телефона
    lte_exists = models.BooleanField() # наличие LTE
    slug = models.SlugField(unique=True) # уникальный идентификатор модели телефона

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)
