from django.db import models
# from django.utils.safestring import mark_safe

# Create your models here.


class Image(models.Model):
    # id = models.AutoField(primary_key=True)
    image = models.TextField()

    # def image_tag(self):  # new
    #     return mark_safe('<img src="/../../media/%s" width="150" height="150" />' % (self.image))

def __str__(self):
    return str(self.id)
