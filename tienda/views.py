from django.shortcuts import render, redirect, get_object_or_404
from .models import Producto, Perfil, Reseña
from .forms import ProductoForm, PerfilForm, CustomUserCreationForm, ImagenPerfilForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm

# Verificar si el usuario es superusuario
def is_superuser(user):
    return user.is_superuser

# Página principal: mostrar productos a todos los usuarios
def index(request):
    productos = Producto.objects.all()  # Mostrar todos los productos
    return render(request, 'paginas/index.html', {'productos': productos})

def carrito(request):
    carrito = request.session.get('carrito', {})
    productos = []
    total = 0

    for producto_id, item in carrito.items():
        producto = get_object_or_404(Producto, id=producto_id)
        cantidad = item.get('cantidad', 1)
        total += producto.precio * cantidad
        productos.append({
            'producto': producto,
            'cantidad': cantidad,
        })

    context = {
        'productos': productos,
        'total': total,
    }

    return render(request, 'paginas/carrito.html', context)

def agregar_al_carrito(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    carrito = request.session.get('carrito', {})

    # Agregar o actualizar producto en el carrito
    if str(producto.id) in carrito:
        carrito[str(producto.id)]['cantidad'] += 1
    else:
        carrito[str(producto.id)] = {
            'nombre': producto.nombre,
            'cantidad': 1,
            'precio': str(producto.precio)
        }

    # Guardar el carrito en la sesión
    request.session['carrito'] = carrito

    # Calcular la cantidad total de productos en el carrito
    cantidad_total = sum(item['cantidad'] for item in carrito.values())

    # Responder con JSON que incluye la cantidad total
    return JsonResponse({'status': 'success', 'cantidad': cantidad_total})

# Aumentar cantidad de un producto en el carrito
def aumentar_cantidad(request, producto_id):
    carrito = request.session.get('carrito', {})

    if str(producto_id) in carrito:
        carrito[str(producto_id)]['cantidad'] += 1
        request.session['carrito'] = carrito

    return redirect('carrito')

# Disminuir cantidad de un producto en el carrito
def disminuir_cantidad(request, producto_id):
    carrito = request.session.get('carrito', {})

    if str(producto_id) in carrito and carrito[str(producto_id)]['cantidad'] > 1:
        carrito[str(producto_id)]['cantidad'] -= 1
        request.session['carrito'] = carrito
    elif str(producto_id) in carrito:
        del carrito[str(producto_id)]

    return redirect('carrito')

def eliminar_del_carrito(request, producto_id):
    carrito = request.session.get('carrito', {})
    
    if str(producto_id) in carrito:
        del carrito[str(producto_id)]
        request.session['carrito'] = carrito
        messages.success(request, "Producto eliminado del carrito")

    return redirect('carrito')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)  # Usa el formulario personalizado
        if form.is_valid():
            user = form.save()
            Perfil.objects.get_or_create(user=user)  # Asegura que el perfil se cree solo si no existe
            login(request, user)
            return redirect('index')
    else:
        form = CustomUserCreationForm()
    return render(request, 'paginas/register.html', {'form': form})

@login_required
def perfil(request):
    perfil = request.user.perfil  # Asegúrate de acceder al perfil del usuario
    if request.method == 'POST':
        form = ImagenPerfilForm(request.POST, request.FILES, instance=perfil)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tu foto de perfil ha sido actualizada.')
            return redirect('perfil')
    else:
        form = ImagenPerfilForm(instance=perfil)
    
    context = {
        'user': request.user,
        'form': form,
    }
    return render(request, 'perfil.html', context)

# Listar productos - solo accesible por el superusuario
@user_passes_test(is_superuser)
@login_required
def productos(request):
    productos = Producto.objects.all()
    return render(request, 'paginas/productos_list.html', {'productos': productos})

@user_passes_test(is_superuser)
@login_required
def agregar_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('productos')
    else:
        form = ProductoForm()
    return render(request, 'paginas/producto_form.html', {'form': form})

@user_passes_test(is_superuser)
@login_required
def editar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('productos')
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'paginas/producto_form.html', {'form': form})

@user_passes_test(is_superuser)
@login_required
def eliminar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        producto.delete()
        return redirect('productos')
    return render(request, 'paginas/producto_confirm_delete.html', {'producto': producto})

@login_required
def editar_perfil(request):
    perfil = get_object_or_404(Perfil, user=request.user)
    if request.method == 'POST':
        form = PerfilForm(request.POST, request.FILES, instance=perfil)
        if form.is_valid():
            form.save()
            return redirect('perfil')
    else:
        form = PerfilForm(instance=perfil)
    return render(request, 'paginas/editar_perfil.html', {'form': form})

def detalle_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    reseñas = producto.reseñas.all()  # Obtener reseñas del producto

    if request.method == 'POST' and request.user.is_authenticated:
        texto = request.POST.get('texto')
        valoracion = request.POST.get('valoracion')
        if texto and valoracion:
            Reseña.objects.create(
                producto=producto,
                usuario=request.user,
                texto=texto,
                valoracion=int(valoracion),  # Guarda la valoración como entero
                fecha=timezone.now()
            )
            return redirect('detalle_producto', id=producto.id)  # Redirige para evitar reenvíos

    # Dividir la descripción en líneas
    descripcion_lines = producto.descripcion.split("\n")  # Asegúrate de que la descripción tenga saltos de línea

    return render(request, 'paginas/detalle_producto.html', {
        'producto': producto,
        'reseñas': reseñas,
        'descripcion_lines': descripcion_lines,  # Pasar la lista de líneas
    })

def buscar_productos(request):
    query = request.GET.get('q')  # Obtener la consulta de búsqueda
    resultados = Producto.objects.filter(nombre__icontains=query) if query else []  # Filtrar productos
    return render(request, 'paginas/buscar_productos.html', {'resultados': resultados, 'query': query})

def pagar(request):
    # Lógica para procesar el pago aquí (puede ser vacía para esta demostración)
    request.session['carrito'] = {}  # Vacía el carrito en la sesión
    messages.success(request, "Compra completada exitosamente")
    return redirect('carrito')
