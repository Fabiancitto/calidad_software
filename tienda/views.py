from django.shortcuts import render, redirect, get_object_or_404
from .models import Producto, Perfil
from .forms import ProductoForm, PerfilForm, CustomUserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse

# Verificar si el usuario es superusuario
def is_superuser(user):
    return user.is_superuser

# Página principal: mostrar productos a todos los usuarios
def index(request):
    productos = Producto.objects.all()  # Mostrar todos los productos
    return render(request, 'paginas/index.html', {'productos': productos})

# Vista del carrito de compras
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

# Agregar un producto al carrito
def agregar_al_carrito(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    carrito = request.session.get('carrito', {})

    if str(producto.id) in carrito:
        carrito[str(producto.id)]['cantidad'] += 1
    else:
        carrito[str(producto.id)] = {'cantidad': 1}

    request.session['carrito'] = carrito
    return JsonResponse({'status': 'success', 'message': 'Producto añadido al carrito'})

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

# Eliminar un producto del carrito
def eliminar_del_carrito(request, producto_id):
    carrito = request.session.get('carrito', {})

    if str(producto_id) in carrito:
        del carrito[str(producto_id)]
        request.session['carrito'] = carrito

    return redirect('carrito')

# Registro de usuario (actualizado)
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Perfil creado automáticamente por la señal, no es necesario hacerlo aquí.
            login(request, user)
            return redirect('index')
    else:
        form = CustomUserCreationForm()

    return render(request, 'paginas/register.html', {'form': form})

@login_required
def perfil(request):
    try:
        perfil = request.user.perfil
    except Perfil.DoesNotExist:
        # Si el perfil no existe, lo creamos automáticamente
        perfil = Perfil.objects.create(user=request.user)
    
    return render(request, 'paginas/perfil.html', {'perfil': perfil, 'user': request.user})

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
