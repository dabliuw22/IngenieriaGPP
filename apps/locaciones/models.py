from django.db import models

# Create your models here.

class Pais(models.Model):
	nombre = models.CharField(max_length = 100)

	def __str__(self):
		return '{}'.format(self.nombre)

class Ciudad(models.Model):
	nombre = models.CharField(max_length = 100)
	pais = models.ForeignKey(Pais, on_delete = models.CASCADE)

	def __str__(self):
		return '{}'.format(self.nombre)