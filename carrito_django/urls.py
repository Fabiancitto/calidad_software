from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from tienda import views

urlpatterns = [
    path('admin/', admin.site.urls),  # Asegúrate de incluir la ruta del administrador
    path('', views.index, name='index'),  # Página principal para ver productos
    path('carrito/', views.carrito, name='carrito'),  # Vista del carrito de compras
    path('agregar_al_carrito/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),  # Agregar al carrito
    path('aumentar_cantidad/<int:producto_id>/', views.aumentar_cantidad, name='aumentar_cantidad'),  # Aumentar cantidad de producto
    path('disminuir_cantidad/<int:producto_id>/', views.disminuir_cantidad, name='disminuir_cantidad'),  # Disminuir cantidad de producto
    path('eliminar_del_carrito/<int:producto_id>/', views.eliminar_del_carrito, name='eliminar_del_carrito'),  # Eliminar del carrito
    
    # Vistas para superusuarios (administradores)
    path('productos/', views.productos, name='productos'),  # Listar productos (solo admin)
    path('agregar_producto/', views.agregar_producto, name='agregar_producto'),  # Agregar productos (solo admin)
    path('editar_producto/<int:pk>/', views.editar_producto, name='editar_producto'),  # Editar productos (solo admin)
    path('eliminar_producto/<int:pk>/', views.eliminar_producto, name='eliminar_producto'),  # Eliminar productos (solo admin)
    
    # Autenticación
    path('register/', views.register, name='register'),  # Registro de usuarios
    path('login/', auth_views.LoginView.as_view(template_name='paginas/login.html'), name='login'),  # Inicio de sesión
    path('logout/', auth_views.LogoutView.as_view(next_page='index'), name='logout'),  # Cerrar sesión
    
    # Perfil de usuario
    path('perfil/', views.perfil, name='perfil'),  # Vista del perfil del usuario
    path('editar_perfil/', views.editar_perfil, name='editar_perfil'),  # Editar perfil (incluyendo la imagen de perfil)
]

# Para servir archivos estáticos y multimedia en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
