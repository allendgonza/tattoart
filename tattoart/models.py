from django.db import models
from django.contrib.auth.models import User

class Producto(models.Model):
    CATEGORIAS = (
        ('maquinas', 'Máquinas'),
        ('tintas', 'Tintas'),
        ('agujas', 'Agujas'),
        ('insumos', 'Insumos'),
        ('guantes', 'Guantes'),
    )
    
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    imagen = models.ImageField(upload_to='productos/')
    categoria = models.CharField(max_length=20, choices=CATEGORIAS)

    def __str__(self):
        return self.nombre

class Carrito(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Carrito de {self.usuario.username}"

class ItemCarrito(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre}"

class Tatuaje(models.Model):
    ESTILOS = (
        ('old-school', 'Old School'),
        ('tribal', 'Tribal'),
        ('irezumi', 'Irezumi'),
        ('realista', 'Realista'),
        ('3d', '3D'),
    )
    
    estilo = models.CharField(max_length=20, choices=ESTILOS)
    descripcion = models.TextField()
    imagen = models.ImageField(upload_to='tatuajes/')

    def __str__(self):
        return f"{self.estilo} - {self.descripcion}"
    

class Contacto(models.Model):
    nombre = models.CharField(max_length=100)
    correo_electronico = models.EmailField()
    mensaje = models.TextField()

    def __str__(self):
        return self.nombre
