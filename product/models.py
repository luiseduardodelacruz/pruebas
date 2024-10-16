from django.db import models

class Sucursales(models.Model):
    id_branch = models.AutoField(primary_key=True) 
    name_branch = models.CharField(max_length=50)
    direccion = models.CharField(max_length=255)
    latitud = models.FloatField()
    longitud = models.FloatField()
    class Meta:
        db_table = 'sucursales'

    def  __str__(self):
        return self.name_branch

class Alcaldia(models.Model):
    id_alcaldia = models.AutoField(primary_key=True)
    nombre_alcaldia = models.CharField(max_length=50)
    latitudes = models.FloatField()
    longitudes = models.FloatField()
    direccion = models.CharField(max_length=255)

    class Meta:
            db_table = 'alcaldias'

    def __str__(self):
        return self.nombre_alcaldia


class Prediccion(models.Model):
    id = models.AutoField(primary_key=True)
    fecha = models.DateField(auto_now_add=True)
    id_branch= models.ForeignKey(Sucursales, on_delete=models.CASCADE, related_name='predicciones')
    id_alcaldia= models.IntegerField()
    id_chain = models.IntegerField()
    cantidad_capistrano = models.IntegerField()
    cantidad_fud = models.IntegerField()
    cantidad_san_rafael = models.IntegerField()
    cantidad_lala = models.IntegerField()
    cantidad_villita = models.IntegerField()
    cantidad_zwan = models.IntegerField()
    cantidad_bafar = models.IntegerField()
    cantidad_chimex = models.IntegerField()
    cantidad_kir = models.IntegerField()
    cantidad_sabori = models. IntegerField()
    total_productos = models.IntegerField()

    class Meta:
        db_table = 'prediccion'  # Especificar el nombre de la tabla

    def __str__(self):
        return f"Predicción {self.id} en {self.fecha}"
    

class Cadena(models.Model):
    id_chain = models.IntegerField(primary_key=True)
    name_chain = models.CharField(max_length=50)

    class Meta:
        db_table = 'cadenas'

    def __str__(self):
        return self.name_chain
    
class User(models.Model):
    username = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)  # Asegúrate de almacenar contraseñas cifradas

    def __str__(self):
        return self.username
