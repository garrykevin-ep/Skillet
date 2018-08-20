from django.db import models

# Create your models here.

class nav_drop_down(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=50)
	url_namespace = models.CharField(max_length=50)
	class Meta:
		verbose_name = "Nav Dropdown"
		verbose_name_plural = "Nav Dropdown"

	def __str__(self):
	    return self.name

class card(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=50)
	url_namespace = models.CharField(max_length=50)
	class Meta:
	    verbose_name = "card"
	    verbose_name_plural = "cards"

	def __str__(self):
	    return self.name
