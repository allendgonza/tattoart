from django.shortcuts import render, redirect, get_object_or_404
from .models import Producto, Tatuaje, Contacto
from django.template.loader import render_to_string
from django.http import JsonResponse
from .forms import ProductoForm, ContactoForm, TatuajeForm, CustomLoginForm, UserRegistrationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
#import mercadopago
from django.conf import settings




class CustomLoginView(LoginView):
    template_name = 'tattoart/login.html'
    authentication_form = CustomLoginForm

class CustomLogoutView(LogoutView):
    next_page = 'inicio'
    

def inicio(request):
    mensaje_exito = request.session.pop('mensaje_exito', None)
    return render(request, 'tattoart/inicio.html', {'mensaje_exito': mensaje_exito})

def tatuadores(request):
    return render(request, 'tattoart/tatuadores.html')

def galeria(request):
    tatuajes = Tatuaje.objects.all()
    estilos = {
        'Old School': tatuajes.filter(estilo='old-school'),
        'Tribal': tatuajes.filter(estilo='tribal'),
        'Irezumi': tatuajes.filter(estilo='irezumi'),
        'Realista': tatuajes.filter(estilo='realista'),
        '3D': tatuajes.filter(estilo='3d'),
    }
    return render(request, 'tattoart/galeria.html', {'estilos': estilos})

def acercaDe(request):
    return render(request, 'tattoart/acercaDe.html')

def productos(request):
    productos = Producto.objects.all()
    categorias = {
        'Máquinas': productos.filter(categoria='maquinas'),
        'Tintas': productos.filter(categoria='tintas'),
        'Agujas': productos.filter(categoria='agujas'),
        'Insumos': productos.filter(categoria='insumos'),
        'Guantes': productos.filter(categoria='guantes'),
    }
    return render(request, 'tattoart/productos.html', {'categorias': categorias})

def agregar_al_carrito(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    carrito = request.session.get('carrito', {})
    if str(producto_id) in carrito:
        carrito[str(producto_id)] += 1
    else:
        carrito[str(producto_id)] = 1
    request.session['carrito'] = carrito

    items = []
    total = 0
    for producto_id, cantidad in carrito.items():
        producto = get_object_or_404(Producto, id=producto_id)
        items.append({'producto': producto, 'cantidad': cantidad, 'subtotal': producto.precio * cantidad})
        total += producto.precio * cantidad

    html = render_to_string('tattoart/carrito_contenido.html', {'items': items, 'total': total}, request=request)
    return JsonResponse({'html': html})

def ver_carrito_ajax(request):
    carrito = request.session.get('carrito', {})
    items = []
    total = 0
    for producto_id, cantidad in carrito.items():
        producto = get_object_or_404(Producto, id=producto_id)
        items.append({'producto': producto, 'cantidad': cantidad, 'subtotal': producto.precio * cantidad})
        total += producto.precio * cantidad

    html = render_to_string('tattoart/carrito_contenido.html', {'items': items, 'total': total}, request=request)
    return JsonResponse({'html': html})

def eliminar_del_carrito(request, item_id):
    carrito = request.session.get('carrito', {})
    if str(item_id) in carrito:
        del carrito[str(item_id)]
    request.session['carrito'] = carrito

    return actualizar_carrito(request)

def actualizar_carrito(request):
    carrito = request.session.get('carrito', {})
    items = []
    total = 0
    for producto_id, cantidad in carrito.items():
        producto = get_object_or_404(Producto, id=producto_id)
        items.append({'producto': producto, 'cantidad': cantidad, 'subtotal': producto.precio * cantidad})
        total += producto.precio * cantidad

    html = render_to_string('tattoart/carrito_contenido.html', {'items': items, 'total': total}, request=request)
    return JsonResponse({'html': html})

def contacto(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']
        correo_electronico = request.POST['correo_electronico']
        mensaje = request.POST['mensaje']

        # Guardar el mensaje en la base de datos
        Contacto.objects.create(nombre=nombre, correo_electronico=correo_electronico, mensaje=mensaje)

        # Guardar el mensaje de éxito en la sesión
        request.session['mensaje_exito'] = 'Mensaje enviado con éxito'

        # Redirigir a la página de inicio
        return redirect('inicio')

    return render(request, 'tattoart/contacto.html')  # Asegúrate de que siempre retorna un HttpResponse para GET requests

@login_required
def menu_admin(request):
    if not request.user.is_superuser:
        return redirect('inicio')

    productos = Producto.objects.all()
    contactos = Contacto.objects.all()
    tatuajes = Tatuaje.objects.all()

    form_producto = ProductoForm()
    form_tatuaje = TatuajeForm()

    return render(request, 'tattoart/menu_admin.html', {
        'productos': productos,
        'contactos': contactos,
        'tatuajes': tatuajes,
        'form_producto': form_producto,
        'form_tatuaje': form_tatuaje,
    })


@login_required
def crear_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('menu_admin')
    else:
        form = ProductoForm()
    productos = Producto.objects.all()
    contactos = Contacto.objects.all()
    tatuajes = Tatuaje.objects.all()
    return render(request, 'tattoart/menu_admin.html', {
        'form_producto': form,
        'productos': productos,
        'contactos': contactos,
        'tatuajes': tatuajes,
    })

@login_required
def editar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('menu_admin')
    productos = Producto.objects.all()
    contactos = Contacto.objects.all()
    tatuajes = Tatuaje.objects.all()
    form_producto = ProductoForm(instance=producto)
    return render(request, 'tattoart/menu_admin.html', {
        'form_producto': form_producto,
        'productos': productos,
        'contactos': contactos,
        'tatuajes': tatuajes,
    })


@login_required
def eliminar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        producto.delete()
        return redirect('menu_admin')
    return redirect('menu_admin')



@login_required
def crear_tatuaje(request):
    if request.method == 'POST':
        form = TatuajeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('menu_admin')
    else:
        form = TatuajeForm()
    productos = Producto.objects.all()
    contactos = Contacto.objects.all()
    tatuajes = Tatuaje.objects.all()
    return render(request, 'tattoart/menu_admin.html', {
        'form_tatuaje': form,
        'productos': productos,
        'contactos': contactos,
        'tatuajes': tatuajes,
    })


@login_required
def editar_tatuaje(request, pk):
    tatuaje = get_object_or_404(Tatuaje, pk=pk)
    if request.method == 'POST':
        form = TatuajeForm(request.POST, request.FILES, instance=tatuaje)
        if form.is_valid():
            form.save()
            return redirect('menu_admin')
    else:
        form = TatuajeForm(instance=tatuaje)
    
    productos = Producto.objects.all()
    contactos = Contacto.objects.all()
    tatuajes = Tatuaje.objects.all()
    return render(request, 'tattoart/menu_admin.html', {
        'form_tatuaje': form,
        'productos': productos,
        'contactos': contactos,
        'tatuajes': tatuajes,
    })


@login_required
def eliminar_tatuaje(request, pk):
    tatuaje = get_object_or_404(Tatuaje, pk=pk)
    tatuaje.delete()
    return redirect('menu_admin')


@login_required
def eliminar_contacto(request, pk):
    contacto = get_object_or_404(Contacto, pk=pk)
    contacto.delete()
    return redirect('menu_admin')

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            messages.success(request, 'Cuenta creada con éxito. ¡Bienvenido!')
            return redirect('inicio')
        else:
            messages.error(request, 'Error al crear la cuenta. Por favor, inténtalo de nuevo.')
    else:
        form = UserRegistrationForm()
    return render(request, 'tattoart/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'¡Bienvenido {username}!')
                return redirect('inicio')
            else:
                messages.error(request, 'Credenciales incorrectas. Inténtelo de nuevo.')
        else:
            messages.error(request, 'Credenciales incorrectas. Inténtelo de nuevo.')
    else:
        form = AuthenticationForm()
    return render(request, 'tattoart/login.html', {'form': form})

@login_required
def editar_contacto(request, pk):
    contacto = get_object_or_404(Contacto, pk=pk)
    if request.method == 'POST':
        form = ContactoForm(request.POST, instance=contacto)
        if form.is_valid():
            form.save()
            return redirect('menu_admin')
    else:
        form = ContactoForm(instance=contacto)
    productos = Producto.objects.all()
    contactos = Contacto.objects.all()
    tatuajes = Tatuaje.objects.all()
    return render(request, 'tattoart/menu_admin.html', {
        'form_contacto': form,
        'productos': productos,
        'contactos': contactos,
        'tatuajes': tatuajes,
    })


#API MERCADOPAGO

#def iniciar_pago(request):
    #sdk = mercadopago.SDK(settings.MERCADOPAGO_CLIENT_ID, settings.MERCADOPAGO_CLIENT_SECRET)
    #preference_data = {
        #"items": [
            #{
                #"title": "Producto de ejemplo",
                #"quantity": 1,
                #"unit_price": 100.00
            #}
        #],
        #"back_urls": {
            #"success": request.build_absolute_uri('/success/'),
            #"failure": request.build_absolute_uri('/failure/'),
            #"pending": request.build_absolute_uri('/pending/')
        #},
        #"auto_return": "approved",
    #}
    
    #preference_response = sdk.preference().create(preference_data)
    #preference = preference_response["response"]
    
    #return redirect(preference['sandbox_init_point'])
