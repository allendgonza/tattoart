from django.contrib import admin
from .models import Producto, Carrito, ItemCarrito, Tatuaje, Contacto

admin.site.register(Producto)
admin.site.register(Carrito)
admin.site.register(ItemCarrito)
admin.site.register(Tatuaje)
admin.site.register(Contacto)
