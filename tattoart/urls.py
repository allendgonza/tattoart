from django.urls import path
from . import views
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.inicio, name='inicio'),
    path('tatuadores/', views.tatuadores, name='tatuadores'),
    path('galeria/', views.galeria, name='galeria'),
    path('acercaDe/', views.acercaDe, name='acercaDe'),
    path('contacto/', views.contacto, name='contacto'),
    path('productos/', views.productos, name='productos'),
    path('agregar_al_carrito/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('ver_carrito_ajax/', views.ver_carrito_ajax, name='ver_carrito_ajax'),
    path('eliminar_del_carrito/<int:item_id>/', views.eliminar_del_carrito, name='eliminar_del_carrito'),
    path('menu_admin/', views.menu_admin, name='menu_admin'),
    path('crear_tatuaje/', views.crear_tatuaje, name='crear_tatuaje'),
    path('editar_tatuaje/<int:pk>/', views.editar_tatuaje, name='editar_tatuaje'),
    path('eliminar_tatuaje/<int:pk>/', views.eliminar_tatuaje, name='eliminar_tatuaje'),
    path('crear_producto/', views.crear_producto, name='crear_producto'),
    path('editar_producto/<int:pk>/', views.editar_producto, name='editar_producto'),
    path('eliminar_producto/<int:pk>/', views.eliminar_producto, name='eliminar_producto'),
    path('editar_contacto/<int:pk>/', views.editar_contacto, name='editar_contacto'),
    path('eliminar_contacto/<int:pk>/', views.eliminar_contacto, name='eliminar_contacto'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='inicio'), name='logout'),
    path('register/', views.register, name='register'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
